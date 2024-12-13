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

global LogLevel;
LogLevel: int = 0;

class LoggerLevel:

    '''
    Logger level settings
    '''

    none = 0;
    trace = ( 1 << 0 );
    warning = ( 1 << 1 );
    information = ( 1 << 2 );
    debug = ( 1 << 3 );
    error = ( 1 << 4 );
    critical = ( 1 << 5 );

    @staticmethod
    def set( LoggerLevel: int ) -> None:
        '''Set a Logger level'''
        global LogLevel;
        LogLevel |= LoggerLevel;

    @staticmethod
    def clear( LoggerLevel: int ) -> None:
        '''Clear a Logger level'''
        global LogLevel;
        LogLevel &= ~ LoggerLevel;

class Logger():

    '''
    Logger instance
    '''

    module: str = None;

    def __init__( self, module: str = None ):
        self.module = module;

    def __logger__( self, type: str, string: str, LoggerLevel: LoggerLevel, *args ) -> str:

        from mikk.fmt import fmt

        string = '[{}] {}'.format( f'{self.module}::{type}' if self.module else type, string );

        for arg in args:

            string = string.replace( "{}", arg, 1 );

        global LogLevel;

        if LogLevel & ( LoggerLevel ):

            print( string );

        return string;

    def error( self, string: str, *args ) -> str:
        return self.__logger__( "Error", string, LoggerLevel.error, *args );

    def debug( self, string: str, *args ) -> str:
        return self.__logger__( "Debug", string, LoggerLevel.debug, *args );

    def warn( self, string: str, *args ) -> str:
        return self.__logger__( "Warning", string, LoggerLevel.warning, *args );

    def info( self, string: str, *args ) -> str:
        return self.__logger__( "Info", string, LoggerLevel.information, *args );

    def trace( self, string: str, *args ) -> str:
        return self.__logger__( "Trace", string, LoggerLevel.trace, *args );

    def critical( self, string: str, *args ) -> str:
        return self.__logger__( "Critical", string, LoggerLevel.critical, *args );

global g_Logger;
g_Logger = Logger(None);
'''Global Logger instance'''
