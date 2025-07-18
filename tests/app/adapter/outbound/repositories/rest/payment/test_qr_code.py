import unittest
from unittest.mock import patch, MagicMock
from app.adapter.outbound.repositories.rest.payment import qr_code

class TestPaymentMock(unittest.TestCase):
    def test_as_dict_contains_expected_keys(self):
        payment = qr_code.PaymentMock('order123', 100.0)
        d = payment.as_dict
        self.assertIn('date', d)
        self.assertIn('transaction_id', d)
        self.assertIn('approval_status', d)
        self.assertIn('message', d)
        self.assertIn('amount', d)
        self.assertIn('order_id', d)
        self.assertEqual(d['amount'], '100.0')  # amount is converted to string
        self.assertEqual(d['order_id'], 'order123')

    @patch('random.choice', return_value=True)
    def test_is_payment_successful_approved(self, mock_choice):
        payment = qr_code.PaymentMock('order123', 50.0)
        self.assertTrue(payment.approval_status)
        self.assertEqual(payment.message, 'success')

    @patch('random.choice', return_value=False)
    def test_is_payment_successful_refused(self, mock_choice):
        payment = qr_code.PaymentMock('order123', 50.0)
        self.assertFalse(payment.approval_status)
        self.assertEqual(payment.message, 'refused')

class TestQRPayment(unittest.TestCase):
    @patch('app.adapter.outbound.repositories.rest.payment.qr_code.requests.post')
    @patch('app.adapter.outbound.repositories.rest.payment.qr_code.PaymentMock')
    def test_request_payment_success(self, mock_paymentmock, mock_post):
        mock_instance = MagicMock()
        mock_instance.as_dict = {'foo': 'bar'}
        mock_paymentmock.return_value = mock_instance
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = 'ok'
        mock_post.return_value = mock_response

        qr = qr_code.QRPayment()
        result = qr.request_payment('order123', 99.9)
        mock_paymentmock.assert_called_once_with('order123', 99.9)
        mock_post.assert_called_once_with(
            'http://localhost:8000/webhook/mercadopago',
            json={'foo': 'bar'},
            timeout=30
        )
        # Check that result is a JSONResponse with the expected content
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.body.decode(), '{"message":"ok"}')

    @patch('app.adapter.outbound.repositories.rest.payment.qr_code.requests.post')
    @patch('app.adapter.outbound.repositories.rest.payment.qr_code.PaymentMock')
    def test_request_payment_raises_for_status(self, mock_paymentmock, mock_post):
        mock_instance = MagicMock()
        mock_instance.as_dict = {'foo': 'bar'}
        mock_paymentmock.return_value = mock_instance
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception('fail')
        mock_post.return_value = mock_response

        qr = qr_code.QRPayment()
        with self.assertRaises(Exception):
            qr.request_payment('order123', 99.9)

if __name__ == '__main__':
    unittest.main()
