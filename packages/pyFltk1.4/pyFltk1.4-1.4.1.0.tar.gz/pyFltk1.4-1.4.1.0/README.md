pyFLTK:
=======

A Python Wrapper for the FLTK library
-------------------------------------

GOALS:

* To wrap FLTK1.4 in Python 
* To port all programs in test/ to Python using pyFLTK
 

If you'd like to help out, I'd suggest using the pyfltk mailing list
(at the bottom) to coordinate who's working on what. 

1) This wrapper requires:

* SWIG 4.0 or later
* Python 3.8 or later
* Fast Light Toolkit 1.4.x-20230728 or later (it should also work with earlier versions)

2) Restrictions

At present, the Python wrapper has been ported and is quite stable. You might encounter certain parts that are not yet or only partailly wrapped.

   

3) The wrapper is available on PyPi: https://pypi.org/project/pyFltk/

4) To build the wrappers yourself do the following: (see INSTALL for more
   details):
   

	
	python setup.py swig (not required if you downloaded the _WithSwig source)
	
	python setup.py build
	
	python setup.py install
   
   
   You might have to edit setup.py to fit your platform. 
   
   
5) Do the following to run some tests:


	
	cd fltk/test
	
	python hello.py
    or
    python3 hello.py (depending on your platform)


* ./test contains demo programs from the FLTK distribution reimplemented
  in Python.
* You can run ./test/demos.py for a little
  menu of the demos



### On the web:

pyFLTK home page: http://pyfltk.sourceforge.io


### License:

pyFLTK Copyright (C) 2003-2021 Andreas Held and others licensed under the
GNU Library General Public License, version 2.0, June 1991 

This library is free software you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License, version 2.0 as published by the Free Software Foundation.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.

You should have received a copy of the GNU Library General Public
License along with this library if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
USA.


### Leads:

Andreas Held  andreasheld[at]users.sourceforge.net

Robert Arkiletian



### Mailing List:

http://lists.sourceforge.net/lists/listinfo/pyfltk-user


### Thanks:

Especial thanks to Kevin Dalhausen, the originator of pyFLTK. He did
such a good job, the rest was easy.

Many thanks to the creators of fltk (www.fltk.org), the best, fastest
and lightest toolkit there is!

Finally, not to forget the creators of SWIG (www.swig.org) a unique
tool for doing what we've done here.












