"""
Copyright (C) 2024, Jabez Winston C

Embedded Tester Protocol Library - GPIO

Author  : Jabez Winston C <jabezwinston@gmail.com>
License : MIT
Date    : 17-Sep-2024

"""

import struct

class GPIO:
    """GPIO class."""

    code = 1
    ops = {
        'info': 0,
        'init': 1,
        'read': 2,
        'write': 3
    }

    info_cmds = {
        'port_count': 0x01,
        'pin_count' : 0x02,
        'ports'     : 0x03,
        'pins'      : 0x04
    }

    def __init__(self, etp):
        """Initialize GPIO class with an ETP instance."""
        self.etp = etp

    def get_info(self) -> dict:
        """Get GPIO port and pin information.
        
        Returns:
            Dictionary containing GPIO port count and pin information.

        Dictionary format:
            - `port_count` (int): Number of GPIO ports.
            - `info` (list): List of dictionaries containing GPIO port and pin information.
                - `port` (str): GPIO port identifier.
                - `pins` (int): GPIO pins available in the port.
        
        """
        gpio_info_cmd = self.code << 8 | self.ops['info']
        # Get the number of GPIO ports
        cmd = self.etp.frame_packet(gpio_info_cmd, struct.pack('B', self.info_cmds['port_count']))
        self.etp.cmd_queue.put(cmd)
        rsp, _ = self.etp.read_rsp()
        port_count = rsp[1]

        # Get the GPIO pins
        cmd = self.etp.frame_packet(gpio_info_cmd, struct.pack('B', self.info_cmds['pins']))
        self.etp.cmd_queue.put(cmd)
        rsp, _ = self.etp.read_rsp()

        # Use iter to unpack the GPIO pins as a list of tuples
        pins = list(struct.iter_unpack('<BI', rsp[1:]))

        pin_info = []

        for pin in pins:
            pin_info.append({'port': chr(pin[0]), 'pins': self.etp.mask_to_bits(pin[1], 32)})

        return {"port_count": port_count, "info": pin_info}

    def decode_gpio_pin(self, pin: str) -> tuple:
        port = ''
        pin_num = 0

        if pin[0] == 'P' and pin[1] >= 'A' and pin[1] <= 'Z' and len(pin) >= 3:
            port = pin[1]
            pin_num = int(pin[2:])
        elif pin[0] == 'P' and pin[1] >= '0' and pin[1] <= '9' and pin[2] == '.' and pin[3] >= '0' and pin[3] <= '9' and len(pin) >= 4:
            port = pin[1]
            pin_num = int(pin[3:])
        elif pin[0] == '_' and pin[1] >= '0' and pin[1] <= '9' and len(pin) >= 2:
            port = pin[0]
            pin_num = int(pin[1:])
        elif pin[1] >= '0' and pin[1] <= '9' and len(pin) >= 2:
            port = pin[0]
            pin_num = int(pin[1:])

        return port, pin_num
    
    def encode_gpio_pin(self, port, pin_num) -> str:
        if port >= ord('A') and port <= ord('Z'):
            return f"P{chr(port)}{pin_num}"
        elif port >= ord('a') and port <= ord('z'):
            return f"{chr(port)}{pin_num}"
        elif port == ord('_'):
            return f"_{pin_num}"

    def init(self, pin_list: dict) -> int:
        """
        Initialize GPIO pins with the given configuration.

        Args:
            pin_list (dict): A dictionary where keys are GPIO pin identifiers and values are 
                                dictionaries containing configuration options for each pin. 
                                Configuration options include:

                Dictionary format:

                - `mode`: Specifies the direction of the pin ('input' or 'output').

                - `type`: Specifies the pull type of the pin ('pull_up' or 'pull_down').

                - `interrupt`: Specifies the interrupt type for the pin 
                            ('rising_edge', 'falling_edge', or 'both_edges').
        
        Returns:
            Status of the operation.
        """
        gpio_init_cmd = self.code << 8 | self.ops['init']
        dir_mask = 0
        dir_val = 0
        pull_mask = 0
        pull_val = 0
        int_mask = 0
        int_val = 0
        for pin, config in pin_list.items():
            port, pin_num = self.decode_gpio_pin(pin)
            # GPIO dir.
            # Check for "mode" key in config
            if 'mode' in config:
                dir_mask |= (1 << pin_num)
                if config['mode'] == 'input':
                    dir_val |= (1 << pin_num)

            if 'type' in config:
                pull_mask |= (1 << pin_num)
                if config['type'] == 'pull_up':
                    pull_val |= (1 << pin_num)

            if 'interrupt' in config:
                int_mask |= (1 << pin_num)
                if config['interrupt'] == 'rising_edge':
                    int_val |= (1 << pin_num * 2)
                elif config['interrupt'] == 'falling_edge':
                    int_val |= (2 << pin_num * 2)
                elif config['interrupt'] == 'both_edges':
                    int_val |= (3 << pin_num * 2)

        cmd = self.etp.frame_packet(gpio_init_cmd, struct.pack('<BIIIIIQ', ord(port), dir_mask, dir_val, pull_mask, pull_val, int_mask, int_val))
        self.etp.cmd_queue.put(cmd)
        _, status = self.etp.read_rsp()
        return status


    def read(self, pin_list: list[str]) -> dict:
        """Read GPIO pins provided as list.

        Args:
            pin_list: List of GPIO pins to read.

        Returns:
            Dictionary of GPIO pins and their states.

        """
        pin_read = dict()
        gpio_read_cmd = self.code << 8 | self.ops['read']
        pin_mask = 0
        for pin in pin_list:
            port, pin_num = self.decode_gpio_pin(pin)
            # Port mask, pin mask (32 bits)
            pin_mask |= (1 << pin_num)

        cmd = self.etp.frame_packet(gpio_read_cmd, struct.pack('<BI', ord(port), pin_mask))
        self.etp.cmd_queue.put(cmd)
        rsp, _ = self.etp.read_rsp()
        port, pin_mask, port_value = struct.unpack('<BII', rsp)
        pins = self.etp.mask_to_bits(pin_mask, 32)
        for pin in pins:
            pin_read[self.encode_gpio_pin(port, pin)] = (port_value & (1 << pin)) >> pin

        return pin_read
    

    def write(self, pin_state: dict):
        """Write GPIO pins provided as dictionary.

        Args:
            pin_state: Dictionary of GPIO pins and their states.

        """
        gpio_write_cmd = self.code << 8 | self.ops['write']
        port = ''
        port_mask = 0
        port_mask_val = 0
        for pin, state in pin_state.items():
            port, pin_num = self.decode_gpio_pin(pin)
            port_mask |= (1 << pin_num)
            if state:
                port_mask_val |= (1 << pin_num)
        
        cmd = self.etp.frame_packet(gpio_write_cmd, struct.pack('<BII', ord(port), port_mask, port_mask_val))
        self.etp.cmd_queue.put(cmd)
