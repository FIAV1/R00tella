#!/usr/bin/env python

import re


def get_ip_pair(ip_string: str) -> tuple:
	"""
	- Il backslash (\) definisce che il prossimo carattere va interpretato come meta carattere,
	diversamente da come lo si interpreta di solito;
	infatti il punto che segue normalmente vorrebbe dire “un carattere qualsiasi”,
	ma in questo caso significa “un punto”.

	- Le parentesi quadre vengono utilizzate per definire un set di caratteri
	e si può utilizzare in due modi: [XY] oppure [0-9].
	Qualsiasi carattere compreso nelle parentesi può essere confrontato.

	-  L’asterisco ci dice “zero o più di quello che mi precede”.
	Ad esempio la RegEx abc* filtra “ab”, “abc”, “abcc”, e tutto ciò che segue come “abccccccc”.
	"""
	ip_v4 = re.sub('\.[0]*', '.', ip_string[:15])
	ip_v6 = ip_string[16:]
	return ip_v4, ip_v6
