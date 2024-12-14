"""
        gg-transfer - a tool to transfer files encoded in audio via FSK modulation
        Copyright (C) 2024 Matteo Tenca

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__version__ = '0.2.13'
from ._send import Sender
from ._receive import Receiver
from ._exceptions import (GgIOError, GgUnicodeError, GgArgumentsError, GgChecksumError,
                          GgTransferError)
__all__ = ['Sender', 'Receiver', 'GgIOError', 'GgUnicodeError', 'GgArgumentsError',
           'GgChecksumError', 'GgTransferError', '__version__']
