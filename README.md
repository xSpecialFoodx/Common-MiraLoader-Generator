# Common-MiraLoader-Generator
turns a mira loader payload to be a common one that can be embedded with specific payloads.

the way it works is that mira loader is having the whole payload during its code, therefore the whole binary code of the payload is included in it.

so this code works on the mira loader footer and header, and patches them in order for mira loader to be able to be embedded in payloads during runtime of a code, without the need to run the make file in the mira loader.

eventually what you need to do is take the header from the generated file, which is the binary data from 0-0xc000 (not included), and the footer from it, which is the binary data from 0x33_from_last_address-last_address and save them in separate files.

during runtime of a script you can then match the header and footer to the payload you want to embed them in, and then load the bin as header-payload-footer.

in order to find the offsets that the header and footer need to be changed, i already have mine in the script, but if it doesn't match yours, what you need to do is to generate a mira loader for payload x, and then generate mira loader for payload y, and use my Difference-Checker payload in order to see the binary differences.

add the found differences locations to the header and footer offsets accordingly (note: the footer offsets doesn't contain anything, but if you find something then you should add it).

notes:

each set of mira loader header and footer is made of 2 bins files (header's bin and footer's bin) and each set matches a single firmware (since mira loader build is locked to a specific firmware, and due to it it calculates the kernel offsets)
