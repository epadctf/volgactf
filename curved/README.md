Curved - Crypto 200 points
======

As the name suggests we are looking at a challange involving elliptic curve cryptography. The challenges said:

---
``
Curved

This server is willing to perform several commands and cat is among them. However, to execute cat flag we need to provide the signature. We only have signatures for exit and leave commands which is cruelly ironic. Can you help us to get the flag?
curved_server.py
exit.sig
key.public
leave.sig
curved.quals.2017.volgactf.ru:8786
``
---

Inspecting the curved_serer.py we see that it is in fact ECDSA signatures using NISP384 and SHA512. TODO <insert snippets>

Additionally we are provided with the signatures for ``leave`` and ``exit`` commands. We will get back to those shortly. Our goal is to somehow be able to call ``cat flag`` either by creating a valid signature or by tricking the server into accepting our command. Since this is a crypto challenge we persue the signature idea.

Quick and dirty intro to ECDSA
------------------------------

The signatures are ECDSA. We provide a short and informal description of the signature scheme and encurages the reader to consult wikipedia TODO <insert link> for further information

Identifying the weakness
------------------------

Now back to the two signatures provided with the challenge. Looking at the values we see that the first halfs of both signatures are the same TODO <insert signatures>. Recall that an ECDSA signature consists of two parts ``r, s``. Now since ``r`` is the same for the two signatures we know that the random value ``k`` is the same, and this is what we will exploit to calculate the private key ``d``

Calculating the private key
---------------------------

Let ``z = sha512('exit') >> 128`` and ``zmark = sha512('leave') >> 128``. We shift the hashes 128 bits right to get a value in the F_384 (this is the same as is done with the hash in the server)

Now calcualte ``k = (z - zmark) / (s - smark)`` in the modulus order of the NISTP384 curve. Let ``n`` be the order of the curve we calculate

``k = (z - zmark) * (s - smark)^(-1) mod n`

from ``k`` we can now compute d by doing ``(s * k - z mod n) * r^(-1) mod n = dA`` which is the private key

The only thing left is to calculate the signature for ``cat flag`` and retrieve the flag.

``
Solve a puzzle: find an x such that 26 last bits of SHA1(x) are set, len(x)==29 and x[:24]=='a14e7e9fb71dc6ae199c585d'
a14e7e9fb71dc6ae199c585d0CoSG
Enter your command:
15284162780589094897514938829004583199557033736567573187424158962893024593035785187525265081269328574515376501996290 35592731612792516783932035344613252195117525291778339753256725964169293331650412053228745241230914428454647051950171 cat flag
VolgaCTF{N0nce_1s_me@nt_to_be_used_0n1y_Once}
Enter your command:
``

note I have added the entry script for solving te dreaded "puzzle" that is required before being able to interact with the challenge, see ``entry.py``



