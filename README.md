
## dicServer, a multithreaded socket server allowing to query word lists (inflected forms) ##

Author: [Laurent Kevers](https://orcid.org/0000-0001-5058-6706) (University of Corsica).

dicServer is available with default linguistic resources for nine languages, but it is possible to add more. You can also replace or modify these resources. See 'Resources' section for more information.

# Versions #

- *dicServer.py* : uses python package "threading"
- *dicServerV2.py* : another version of dicServer (uses different python packages : multiprocessing)

# Execution #

	python3 dicServer.py WORKING_DIRECTORY

- WORKING_DIRECTORY is the place where the scipt starts; linguistic resources are organized into dedicated directories under this working directory.
- Port is specified into the script (default: **1112**)
- Logging is available into *dicServer.log*

You can query the server within your Python code with the following instructions (see *test_threaded_daemon.py* script) :

	HOST, PORT = "", 1112
	data = " ".join(sys.argv[1:]) # the query is given as arg

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		# Connect to server and send data
		sock.connect((HOST, PORT))
		sock.sendall(("%s\n"%data).encode(encoding='utf-8'))

		# Receive data from the server and shut down
		received = sock.recv(1024)

	finally:
		sock.close()

To shutdown the server get the process id and kill it :

	ps -aux | grep dicServer
	kill <processID>

# Result format #

The result is returned as a json object.


# Querying methods available #

	is_word::WORD
	- For the word given as parameter
	- Returns 'True' if it is present in at least one dictionary
	- Else returns 'False'

	is_lg_word::WORD::LG
	- For a word and a language
	- Returns 'True' if this word exists in the language dictionary
	- Else returns 'False'

	word_languages::WORD
	- For a word
	- Returns a list with all languages for which the word exists in the language dictionary.
	- If the word doesn't exist in any dictionary, returns an empty list

	word_possibleLanguages::WORD::LGlist
	- For a word, and a reduced set of possible languages (LGlist eg. : eng,fra)
	- Returns a list with all languages for which the word exists in the language dictionary.
	- If the word doesn't exist in any dictionary, returns an empty list


# Testing #

Could be performed with the test_threaded_daemon.py script.

Example:

	python3 test_threaded_daemon.py word_languages::car

-> Result: ["cos", "eng", "fra", "nld", "spa"]

# Resources #

The linguistic resources are defined into the script (see 'languages'). They must be stored somewhere under the WORKING_DIRECTORY defined as parameter of dicServer.

The data format is either a simple wordlist (one linguistic form by line) or a Unitex/DELA format. For this last case, the directory path to the language data file must contain the word 'unitex'.

The resources offered by default come from different sources :
- English, Italian, German, French, Portuguese, Spanish
	- Unitex linguistic resources (https://unitexgramlab.org/fr/language-resources or https://github.com/UnitexGramLab/unitex-lingua)
	- **LGPLLR license**
- Dutch
	- Opentaal dictionary (https://github.com/OpenTaal/opentaal-wordlist)
	- **BSD / CC-BY 3.0**
- Romanian
	- Romanian – English parallel wordlists. Created for the European Language Resources Coordination Action (ELRC) by Tufis Dan, Institutul de Cercetari pentru Inteligenta Artificiala 'Mihai Draganescu', Academia Romana (https://elrc-share.eu/repository/browse/romanian-english-parallel-wordlists/)
	- **CC-BY 4.0**
- Corsican
	- Derived from Bible Corpus <!--and from BDLC data-->
	- **CC-BY-SA-NC 4.0**

# dicServer Code License #

The Python codes are released under [CeCILL_V2.1](http://www.cecill.info/licences/Licence_CeCILL_V2.1-fr.html).

