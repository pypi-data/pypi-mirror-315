"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

class jsonc:

    '''
    Json Commentary
    '''

    from mikk.Logger import Logger;
    m_Logger = Logger( "Json" );

    @staticmethod
    def load( object: str, exists_ok = False, except_ok = False, encoding = 'utf-8' ) -> dict | list:

        '''
        Open a json file ignoring single-line commentary

        **object** Path to a json file or a string with json format

        **exists_ok** If true when the file doesn't exist we create it and return a empty dict instead of throwing a warning error

        **except_ok** If true this will return a empty dictionary when a Exception is thrown

        **encoding** Encoding used for reading the file.
        '''

        from os.path import exists;

        filenm = None

        if object.endswith( '.json' ):

            filenm = object;

            if exists( object ):

                with open( file = object, mode = 'r', encoding = encoding ) as __file__:
        
                    object = __file__.readlines();

            elif exists_ok:

                open( object, 'w' ).write( "{\n}" );

                return {};

            else:

                except_ = jsonc.m_Logger.error( "File doesn't exists {}", object );

                if not except_ok:

                    raise Exception( except_ );

                return {};

        from json import loads

        __js_split__ = '';

        if isinstance( object, str ):

            __js_split__ = object;
        
        else:

            for __line__ in object:

                __line__ = __line__.strip();

                if __line__ and __line__ != '':

                    if __line__.startswith( '//' ):

                        jsonc.m_Logger.debug( "Ignoring commentary line {}", __line__ );

                    else:

                        __js_split__ = f'{__js_split__}\n{__line__}';

        try:

            js = loads( __js_split__ );

            return js;

        except Exception as e:

            except_ = jsonc.m_Logger.error( "Can not open {} Exception {}", filenm if filenm else 'object', e );

            if not except_ok:

                raise Exception( except_ );

        return {};
