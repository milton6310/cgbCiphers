class Reflector:
    """Represents a reflector."""

    def __init__(self, wiring=None, name=None, model=None, date=None, debug=False):
        if wiring != None:
            self.wiring = wiring
        else:
            self.wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.name = name
        self.model = model
        self.date = date
        self.debug = debug

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def encipher(self, key):
        shift = ord(self.state) - ord("A")
        index = (ord(key) - ord("A")) % 26  # true index
        index = (index + shift) % 26  # actual connector hit
        letter = self.wiring[index]  # rotor letter generated
        out = chr(ord("A") + (ord(letter) - ord("A") + 26 - shift) % 26)  # actual output
        if self.debug:
            print(self.name,' [---] ', self.state,': ', key,' ', out, sep='');
        # return letter
        return out

    def __eq__(self, rotor):
        return self.name == rotor.name
    
    def __str__(self):
        """Pretty display."""
        return """
        Name: {}
        Model: {}
        Date: {}
        Wiring: {}""".format(
            self.name, self.model, self.date, self.wiring
        )

class Rotor:
    """Represents a rotor."""

    def __init__(
        self,
        wiring=None,
        notchs=None,
        name=None,
        model=None,
        date=None,
        state="A",
        ring="A",
        debug=False,
    ):
        """
        Initialization of the rotor.
        """
        if wiring != None:
            self.wiring = wiring
        else:
            self.wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.rwiring = ["0"] * 26
        for i in range(0, len(self.wiring)):
            self.rwiring[ord(self.wiring[i]) - ord("A")] = chr(ord("A") + i)
        if notchs != None:
            self.notchs = notchs
        else:
            self.notchs = ""
        self.name = name
        self.model = model
        self.date = date
        self.state = state
        self.ring = ring
        self.debug = debug

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name == "wiring":
            self.rwiring = ["0"] * 26
            for i in range(0, len(self.wiring)):
                self.rwiring[ord(self.wiring[i]) - ord("A")] = chr(ord("A") + i)

    def encipher_right(self, key):
        shift = ord(self.state) - ord(self.ring) + 26
        index = (ord(key) - ord("A")) % 26  # true index
        index = (index + shift) % 26  # actual connector hit
        letter = self.wiring[index]  # rotor letter generated
        out = chr(ord("A") + (ord(letter) - ord("A") + 26 - shift) % 26)  # actual output
        if self.debug:
            print(self.name,' [>>>] ', self.state,': ', key,' ', out, sep='');
        return out

    def encipher_left(self, key):
        shift = ord(self.state) - ord(self.ring) + 26
        index = (ord(key) - ord("A")) % 26
        index = (index + shift) % 26
        # mapped output
        letter = self.rwiring[index]
        out = chr(ord("A") + (ord(letter) - ord("A") + 26 - shift) % 26)
        if self.debug:
            print(self.name,' [<<<] ', self.state,': ', key,' ', out, sep='');
        return out

    def notch(self, offset=1):
        r = chr((ord(self.state) + offset - ord("A")) % 26 + ord("A"))
        if self.debug:
            print(self.name,' [notch] ', self.state,' --> ', r, sep='');
        self.state = r
        notchnext = self.state in self.notchs
        return

    def is_in_turnover_pos(self):
        x = chr((ord(self.state) + 1 - ord("A")) % 26 + ord("A"))
        ret = x in self.notchs
        if self.debug:
            print(self.name,' [turnover] ? = ', ret, ', state = ', x, ', notchs = ', self.notchs, sep='');
        return ret

    def __eq__(self, rotor):
        return self.name == rotor.name

    def __str__(self):
        """
        Pretty display.
        """
        return """
        Name: {}
        Model: {}
        Date: {}
        Wiring: {}
        RWiring: {}
        State: {}""".format(
            self.name, self.model, self.date, self.wiring, ''.join(self.rwiring), self.state
        )


# 1924 Rotors
ROTOR_IC = Rotor(
    wiring="DMTWSILRUYQNKFEJCAZBPGXOHV", name="IC", model="Commercial Enigma A, B", date="1924",)
ROTOR_IIC = Rotor(wiring="HQZGPJTMOBLNCIFDYAWVEUSRKX",name="IIC",model="Commercial Enigma A, B",date="1924",)
ROTOR_IIIC = Rotor(wiring="UQNTLSZFMREHDPXKIBVYGJCWOA",name="IIIC",model="Commercial Enigma A, B",date="1924",)

# German Railway Rotors
ROTOR_GR_I = Rotor(wiring="JGDQOXUSCAMIFRVTPNEWKBLZYH",name="I",model="German Railway (Rocket)",date="7 February 1941",)
ROTOR_GR_II = Rotor(wiring="NTZPSFBOKMWRCJDIVLAEYUXHGQ",name="II",model="German Railway (Rocket)",date="7 February 1941",)
ROTOR_GR_III = Rotor(wiring="JVIUBHTCDYAKEQZPOSGXNRMWFL",name="III",model="German Railway (Rocket)",date="7 February 1941",)
ROTOR_GR_UKW = Reflector(wiring="QYHOGNECVPUZTFDJAXWMKISRBL",name="UTKW",model="German Railway (Rocket)",date="7 February 1941",)
ROTOR_GR_ETW = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML",name="ETW",model="German Railway (Rocket)",date="7 February 1941",)

# Swiss SONDER Rotors
ROTOR_I_SONDER = Rotor(wiring="VEOSIRZUJDQCKGWYPNXAFLTHMB",name="I-SONDER",model="Enigma Sonder",date="February 1939",)
ROTOR_II_SONDER = Rotor(wiring="UEMOATQLSHPKCYFWJZBGVXIDNR",name="II-SONDER",model="Enigma Sonder",date="February 1939",)
ROTOR_III_SONDER = Rotor(wiring="TZHXMBSIPNURJFDKEQVCWGLAOY",name="III-SONDER",model="Enigma Sonder",date="February 1939",)
ROTOR_UKW_SONDER = Reflector(wiring="CIAGSNDRBYTPZFULVHEKOQXWJM",name="UKW-SONDER",model="Enigma Sonder",date="February 1939",)
ROTOR_ETW_SONDER = Rotor(wiring="ABCDEFGHIJKLMNOPQRSTUVWXYZ",name="ETW-SONDER",model="Enigma Sonder",date="February 1939",)

# Enigma K Rotors
ROTOR_I_K = Rotor(wiring="LPGSZMHAEOQKVXRFYBUTNICJDW",notchs="G",name="I-K",model="Enigma K",date="February 1939",)
ROTOR_II_K = Rotor(wiring="SLVGBTFXJQOHEWIRZYAMKPCNDU",notchs="M",name="II-K",model="Enigma K",date="February 1939",)
ROTOR_III_K = Rotor(wiring="CJGDPSHKTURAWZXFMYNQOBVLIE",notchs="V",name="III-K",model="Enigma K",date="February 1939",)
ROTOR_UKW_K = Reflector(wiring="IMETCGFRAYSQBZXWLHKDVUPOJN",name="UKW-K",model="Enigma K",date="February 1939",)
ROTOR_ETW_K = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML",name="ETW-K",model="Enigma K",date="February 1939",)

# Enigma G Rotors, turnover: 'SUVWZABCEFGIKLOPQ', 'STVYZACDFGHKMNQ', 'UWXAEFHKMNR'
ROTOR_I_G = Rotor(wiring="LPGSZMHAEOQKVXRFYBUTNICJDW",notchs="ACDEHIJKMNOQSTWXY",name="I-G",model="Enigma G",date="",)
ROTOR_II_G = Rotor(wiring="SLVGBTFXJQOHEWIRZYAMKPCNDU",notchs="ABDGHIKLNOPSUVY",name="II-G",model="Enigma G",date="",)
ROTOR_III_G = Rotor(wiring="CJGDPSHKTURAWZXFMYNQOBVLIE",notchs="CEFIMNPSUVZ",name="III-G",model="Enigma G",date="",)
ROTOR_UKW_G = Reflector(wiring="IMETCGFRAYSQBZXWLHKDVUPOJN",name="UKW-G",model="Enigma G",date="",)
ROTOR_ETW_G = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML",name="ETW-G",model="Enigma G",date="",)

# Enigma R(ailway) Rotors
ROTOR_I_R = Rotor(wiring="JGDQOXUSCAMIFRVTPNEWKBLZYH",notchs="V",name="I-R",model="Enigma R",date="February 1939",)
ROTOR_II_R = Rotor(wiring="NTZPSFBOKMWRCJDIVLAEYUXHGQ",notchs="M",name="II-R",model="Enigma R",date="February 1939",)
ROTOR_III_R = Rotor(wiring="JVIUBHTCDYAKEQZPOSGXNRMWFL",notchs="G",name="III-R",model="Enigma R",date="February 1939",)
ROTOR_UKW_R = Reflector(wiring="QYHOGNECVPUZTFDJAXWMKISRBL",name="UKW-R",model="Enigma R",date="February 1939",)
ROTOR_ETW_R = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML",name="ETW-R",model="Enigma R",date="February 1939",)

# Swiss K Rotors
ROTOR_I_SK = Rotor(wiring="PEZUOHXSCVFMTBGLRINQJWAYDK",notchs="G",name="I-K",model="Swiss K",date="February 1939",)
ROTOR_II_SK = Rotor(wiring="ZOUESYDKFWPCIQXHMVBLGNJRAT",notchs="M",name="II-K",model="Swiss K",date="February 1939",)
ROTOR_III_SK = Rotor(wiring="EHRVXGAOBQUSIMZFLYNWKTPDJC",notchs="V",name="III-K",model="Swiss K",date="February 1939",)
ROTOR_UKW_SK = Reflector(wiring="IMETCGFRAYSQBZXWLHKDVUPOJN",name="UKW-K",model="Swiss K",date="February 1939",)
ROTOR_ETW_SK = Rotor(wiring="QWERTZUIOASDFGHJKPYXCVBNML",name="ETW-K",model="Swiss K",date="February 1939",)

# Enigma
ROTOR_I = Rotor(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ",notchs="R",name="I",model="Enigma 1",date="1930",)
ROTOR_II = Rotor(wiring="AJDKSIRUXBLHWTMCQGZNPYFVOE",notchs="F",name="II",model="Enigma 1",date="1930",)
ROTOR_III = Rotor(wiring="BDFHJLCPRTXVZNYEIWGAKMUSQO",notchs="W",name="III",model="Enigma 1",date="1930",)
ROTOR_IV = Rotor(wiring="ESOVPZJAYQUIRHXLNFTGKDCMWB",notchs="K",name="IV",model="M3 Army",date="December 1938",)
ROTOR_V = Rotor(wiring="VZBRGITYUPSDNHLXAWMJQOFECK",notchs="A",name="V",model="M3 Army",date="December 1938",)
ROTOR_VI = Rotor(wiring="JPGVOUMFYQBENHZRDKASXLICTW",notchs="AN",name="VI",model="M3 & M4 Naval(February 1942)",date="1939",)
ROTOR_VII = Rotor(wiring="NZJHGRCXMYSWBOUFAIVLPEKQDT",notchs="AN",name="VII",model="M3 & M4 Naval(February 1942)",date="1939",)
ROTOR_VIII = Rotor(wiring="FKQHTLXOCBJSPDZRAMEWNIUYGV",notchs="AN",name="VIII",model="M3 & M4 Naval(February 1942)",date="1939",)

# misc & reflectors
ROTOR_Beta = Rotor(
    wiring="LEYJVCNIXWPBQMDRTAKZGFUHOS", name="Beta", model="M4 R2", date="Spring 1941"
)
ROTOR_Gamma = Rotor(
    wiring="FSOKANUERHMBTIYCWLQPZXVGJD", name="Gamma", model="M4 R2", date="Spring 1941"
)
ROTOR_Reflector_A = Reflector(wiring="EJMZALYXVBWFCRQUONTSPIKHGD", name="Reflector A")
ROTOR_Reflector_B = Reflector(wiring="YRUHQSLDPXNGOKMIEBFZCWVJAT", name="Reflector B")
ROTOR_Reflector_C = Reflector(wiring="FVPJIAOYEDRZXWGCTKUQSBNMHL", name="Reflector C")
ROTOR_Reflector_B_Thin = Reflector(
    wiring="ENKQAUYWJICOPBLMDXZVFTHRGS",
    name="Reflector_B_Thin",
    model="M4 R1 (M3 + Thin)",
    date="1940",
)
ROTOR_Reflector_C_Thin = Reflector(
    wiring="RDOBJNTKVEHMLFCWZAXGYIPSUQ",
    name="Reflector_C_Thin",
    model="M4 R1 (M3 + Thin)",
    date="1940",
)
ROTOR_ETW = Rotor(wiring="ABCDEFGHIJKLMNOPQRSTUVWXYZ", name="ETW", model="Enigma 1")