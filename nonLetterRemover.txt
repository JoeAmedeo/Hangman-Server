#include <iostream>
#include <fstream>
#include <string>

/* This small program can be used in conjunction with a text file in order to remove any lines in said file that have a non-letter character in them.
In the english dictionary, the only non-letter characters that you will see are (, ), -, and '. which can be represented with ascii character #'s 
char(40), char(41), char(45), and char(39) respectively. */

int main() {

	/* open input stream for old file and output stream for new letter only file */
	std::ifstream oldTextFile;
	std::ofstream newTextFile;
	oldTextFile.open("wordlist.txt");
	newTextFile.open("newWordList.txt");

	std::string currentLine; 
	bool onlyLetters;
	/*maintain loop while output stream is still open */
	while (newTextFile.is_open()) {
		while (getline(oldTextFile, currentLine)) {
			onlyLetters = true;
			/* iterate over every character of each line */
			for (int i = 0; i < currentLine.length(); i++) {
				/* set marker to false if one of the three non-letter characters is within the string */
				if (currentLine.at(i) == '-' || currentLine.at(i) ==  '(' || currentLine.at(i) ==  ')' || currentLine.at(i) == char(39)) {
					onlyLetters = false;
				}
			}
			/* write current line to new file if all characters in the string where letters */
			if (onlyLetters) {
				std::cout << currentLine << '\n';
				newTextFile << currentLine << '\n';
			}
		}


	}

}