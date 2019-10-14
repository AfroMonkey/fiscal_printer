# -*- coding: utf-8 -*-
############################################################################
#    Coded by: Moisés Navarro (https://github.com/AfroMonkey)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Fiscal Printer',
    'version': '1.1.0',
    'author': 'Moisés Navarro',
    'website': 'https://github.com/AfroMonkey',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/pos_config.xml',
        'templates/fiscal_printer.xml',
    ],
    'qweb': [
        'static/src/xml/fiscal_printer.xml',
    ],
}
