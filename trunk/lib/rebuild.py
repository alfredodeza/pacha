# Copyright 2009 Alfredo Deza
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Does all the rebuilding work when a host needs to be reconstructed 
with Pacha. Minimal configurations come from pacha.conf and more complex
executions come from the sh folder."""

class Config(object):
    """Reads pacha.conf and executes the values"""

class Sh(object):
    """Executes all the *.sh scripts in the sh folder"""



