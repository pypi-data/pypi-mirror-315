import unittest
from unittest.mock import patch, MagicMock
from modbus_jaka.Jaka_Coms import ModbusHelper
from pymodbus.exceptions import ModbusException

class TestModbusHelper(unittest.TestCase):

    @patch('modbus_jaka.modbus_helper.ModbusTcpClient')
    def test_read_input_1(self, mock_tcp_client):
        """
        Test reading the state of input 1 specifically.
        Input 1 is mapped to Modbus address 8.
        """
        # Mock the client connection
        instance = mock_tcp_client.return_value
        instance.connect.return_value = True

        # Mock response for read_discrete_inputs (simulating the server returns True for input 1)
        mock_response = MagicMock()
        mock_response.isError.return_value = False
        mock_response.bits = [True]  # Single bit representing the state
        instance.read_discrete_inputs.return_value = mock_response

        helper = ModbusHelper(host="192.168.1.101", port=502)

        state = helper.read_input_state(1)  # This should map to address 8
        self.assertTrue(state, "Expected state for input 1 to be True")

        # Ensure the call was made with address=8 and count=1
        instance.read_discrete_inputs.assert_called_with(address=8, count=1)

        # Clean up
        helper.close()

    @patch('modbus_jaka.modbus_helper.ModbusTcpClient')
    def test_read_input_state_invalid_range(self, mock_tcp_client):
        """
        Test that ValueError is raised for input numbers out of valid range [1..128].
        """
        instance = mock_tcp_client.return_value
        instance.connect.return_value = True

        helper = ModbusHelper(host="192.168.1.101", port=502)

        with self.assertRaises(ValueError):
            helper.read_input_state(0)   # out of range
        with self.assertRaises(ValueError):
            helper.read_input_state(129) # out of range

        helper.close()

    @patch('modbus_jaka.modbus_helper.ModbusTcpClient')
    def test_read_input_state_error_response(self, mock_tcp_client):
        """
        Test that a ModbusException is raised when the server returns an error response.
        """
        instance = mock_tcp_client.return_value
        instance.connect.return_value = True

        # Mock the server response to indicate an error
        mock_response = MagicMock()
        mock_response.isError.return_value = True
        instance.read_discrete_inputs.return_value = mock_response

        helper = ModbusHelper(host="192.168.1.101", port=502)

        with self.assertRaises(ModbusException):
            helper.read_input_state(1)

        helper.close()

if __name__ == '__main__':
    unittest.main()
