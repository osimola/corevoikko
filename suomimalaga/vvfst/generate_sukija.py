# -*- coding: utf-8 -*-

# Copyright 2013-2014 Hannu Väisänen (Hannu.Vaisanen@uef.fi)
# Program to generate old spellings and common spelling mistakes for Voikko lexicon.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# This program generates old spellings (e.g. symbooli) and
# common spelling errors (e.g. kirjottaa) from file "all.lexc".
#
# An example: from line
# [Ln][Xp]symboli[X]symbol@P.INEN_SALLITTU.ON@:symbol@P.INEN_SALLITTU.ON@ NimisanaPaperi_a ;
#
# generate line
# [Ln][Xp]symboli[X]symbool@P.INEN_SALLITTU.ON@:symbool@P.INEN_SALLITTU.ON@ NimisanaPaperi_a 
#
# Shoud I generate these lines also?
# [Ln][Xp]symbooli[X]symbol@P.INEN_SALLITTU.ON@:symbol@P.INEN_SALLITTU.ON@ NimisanaPaperi_a ;
# [Ln][Xp]symbooli[X]symbool@P.INEN_SALLITTU.ON@:symbool@P.INEN_SALLITTU.ON@ NimisanaPaperi_a 
#
# This automatic generation will generate some old
# spellings and spelling errors that do not exist in real life.

# Compiling (in directory suomimalaga):
# make vvfst-sukija; make vvfst-sukija-install DESTDIR=~/vvfst/voikkodict/

# Compiling (in directory suomimalaga/vvfst):
# cd ..; make vvfst-sukija; make vvfst-sukija-install DESTDIR=~/vvfst/voikkodict/; cd vvfst

# Testing (in directory suomimalaga/vvfst):
# foma -e "read att all-sukija.att" -e "save stack sukija.fst" -e "quit"
# date; cat ~/Lataukset/koesanat?.txt | flookup -i sukija.fst | gawk 'length($0) > 0' | sort >test.out; date
# diff test.out ~/Lataukset/vvfst-sukija-testi.out | grep '<.*[+][?]' | less
# diff test.out ~/Lataukset/vvfst-sukija-testi.out | grep '>.*[+][?]' | less
# diff test.out ~/Lataukset/vvfst-sukija-testi.out | grep '>.*[+][?]' | gawk '{print $2}' |flookup -i sukija.fst | gawk 'length($0) > 0'
# cp test.out ~/Lataukset/vvfst-sukija-testi.out

# Style- ja usage-lippujen arvot suoraan Joukahaisesta:
# grep -A1 '<style>' ../vocabulary/joukahainen.xml|grep flag|sort -u|gawk '{printf "%s,", substr($1,7,length($1)-13)}'
# grep -A1 '<usage>' ../vocabulary/joukahainen.xml|grep flag|sort -u|gawk '{printf "%s,", substr($1,7,length($1)-13)}'


import codecs
import getopt
import re
import sys
from types import *
sys.path.append("common")
import generate_lex_common

OPTIONS = generate_lex_common.get_options()

infile = codecs.open (OPTIONS["destdir"] + u"/all.lexc", "r", "UTF-8")
outfile = codecs.open (OPTIONS["destdir"] + u"/all-sukija.lexc", 'w', 'UTF-8')
sukijafile = codecs.open (OPTIONS["destdir"] + u"/poikkeavat-sukija.lexc", 'r', 'UTF-8')

C = u"[qwrtpsšdfghjklzžxcvbnm]"  # Consonants.
V = u"[aeiouüyåäö]"              # Vovels.
A = u"[aä]"
U = u"[uy]"

def makeRePattern (wordClass, word):
    u = u"^\\[%s\\]\\[Xp\\].*%s\\[X\\]" % (wordClass, word)
    u = u.replace ('C', C)
    u = u.replace ('V', V)
    u = u.replace ('A', A)
    u = u.replace ('U', U)
    return u


def makeRe (wordClass, word):
    return re.compile (makeRePattern (wordClass, word), re.UNICODE)


def replace (s, old, new):
    u = s.replace (old + u":", new + u":")
    u = u.replace (old + u" ", new + u" ")
    u = u.replace (old + u"\t", new + u"\t")
    u = u.replace (old + u"@", new + u"@")
    return u


def replace_and_write (line, string1, string2):
    s = replace (line, string1, string2)
    outfile.write (s)


re_adi = makeRe (u"Ln", u".Cadi")
re_odi = makeRe (u"Ln", u".Codi")
re_ofi = makeRe (u"Ln", u".Cofi")
re_ogi = makeRe (u"Ln", u".Cogi")
re_oli = makeRe (u"Ln", u".Coli")
re_omi = makeRe (u"Ln", u".Comi")
re_oni = makeRe (u"Ln", u".Coni")
re_ori = makeRe (u"Ln", u".Cori")

re_OOri = makeRe (u"Ln", u".Cööri")
re_UUri = makeRe (u"Ln", u"..UUri")

re_adinen = makeRe (u"Ln", u".Cadinen")
re_odinen = makeRe (u"Ln", u".Codinen")
re_ofinen = makeRe (u"Ln", u".Cofinen")
re_oginen = makeRe (u"Ln", u".Coginen")
re_olinen = makeRe (u"Ln", u".Colinen")
re_ominen = makeRe (u"Ln", u".Cominen")
re_oninen = makeRe (u"Ln", u".Coninen")
re_orinen = makeRe (u"Ll", u".Corinen")

re_grafia   = makeRe (u"Ln", u"grafia")
re_grafinen = makeRe (u"Ll", u"grafinen")
re_logia    = makeRe (u"Ln", u"logia")
re_loginen  = makeRe (u"Ll", u"loginen")

re_oittaa1 = makeRe (u"Lt", u".Coittaa")
re_oittaa2 = makeRe (u"Lt", u".Cöittää")

re_ottaa1 = makeRe (u"Lt", u".Cottaa")
re_ottaa2 = makeRe (u"Lt", u".Cöttää")

re_oitin = makeRe (u"Ln", u".Coitin")
re_aatio = makeRe (u"Ln", u".Caatio")
re_uutio = makeRe (u"Ln", u".Cuutio")
re_uusio = makeRe (u"Ln", u".Cuusio")
re_tio   = makeRe (u"Ln", u"([^a]i|k)tio") # Traditio, funktio, mutta ei aitio.

re_toninen = makeRe (u"Ll", u".toninen")
re_iivinen = makeRe (u"Ll", u"Ciivinen")
re_aalinen = makeRe (u"Ll", u"aalinen")

re_nuolaista = re.compile (u"\\[Lt\\].* Nuolaista_", re.UNICODE)
re_rangaista = re.compile (u"\\[Lt\\].* Rangaista_", re.UNICODE)

re_Xiljoona = re.compile (u"\\A(?:\\[Bc\\]|\\[Sn\\]|@).*(b|m|tr)iljoon", re.UNICODE)

re_eikAs = makeRe (u"Ll", u"eikAs")


# Words to be excluded.
#
re_adi_x = re.compile (u"\\A\[Ln\]\[Xp\](faradi|pikofaradi|stadi)\[X\]")
re_ogi_x = re.compile (u"\\A\[Ln\]\[Xp\](blogi|grogi|judogi)\[X\]")
re_omi_x = re.compile (u"\\A\[Ln\]\[Xp\](binomi|bromi|dibromi|genomi|kromi|trinomi)\[X\]")
re_oni_x = re.compile (u"\\A\[Ln\]\[Xp\](ikoni)\[X\]")
re_ori_x = re.compile (u"\\A\[Ln\]\[Xp\](hevosori|jalostusori|reettori|siitosori)\[X\]")

re_logia_x = re.compile (u"\\A\[Ln\]\[Xp\](genealogia|trilogia)\[X\]")

re_A = re.compile (u"[aou]")


spelling_pattern_list = [
  (re_adi, u"ad", u"aad", re_adi_x),  # Serenadi  => senenaadi.
  (re_odi, u"od", u"ood"),            # Aplodi    => aploodi.
  (re_ofi, u"of", u"oof"),            # Filosofi  => filosoofi.
  (re_ogi, u"og", u"oog", re_ogi_x),  # Arkeologi => arkeoloogi.
  (re_oli, u"ol", u"ool"),            # Symboli   => symbooli.
  (re_omi, u"om", u"oom", re_omi_x),  # Atomi     => atoomi.
  (re_oni, u"on", u"oon", re_oni_x),  # Telefoni  => telefooni.
  (re_ori, u"or", u"oor", re_ori_x),  # Pehtori   => pehtoori.

  (re_OOri,     u"öör",   u"ör"),     # Amatööri => amatöri.
  (re_UUri,     u"uur",   u"ur"),

  (re_adinen,   u"adi",    u"aadi"),
  (re_odinen,   u"odi",    u"oodi"),
  (re_ofinen,   u"ofi",    u"oofi"),
  (re_oginen,   u"ogi",    u"oogi"),
  (re_olinen,   u"oli",    u"ooli"),
  (re_ominen,   u"omi",    u"oomi"),
  (re_oninen,   u"oni",    u"ooni"),
  (re_orinen,   u"ori",    u"oori"),

  (re_grafia,   u"grafi",  u"graafi"),
  (re_grafinen, u"grafi",  u"graafi"),
  (re_logia,    u"logi",   u"loogi", re_logia_x),
  (re_loginen,  u"logi",   u"loogi"),

  (re_oitin, u"oit", u"ot"),  # Kirjoitin => kirjotin (esim. kirjo(i)ttimen).
  (re_oittaa1, u"o",   u"ot",  u"Kirjoittaa", u"Alittaa"),
  (re_oittaa2, u"ö",   u"öt",  u"Kirjoittaa", u"Alittaa"),
  (re_oittaa1, u"oit", u"ot",  u"Alittaa",    u"Alittaa"),
  (re_oittaa2, u"öit", u"öt",  u"Alittaa",    u"Alittaa"),
  (re_ottaa1,  u"ot",  u"oit", u"Alittaa",    u"Alittaa"),
  (re_ottaa2,  u"öt",  u"öit", u"Alittaa",    u"Alittaa"),
  (re_ottaa1,  u"o",   u"oi",  u"Ammottaa",   u"Ammottaa"),
  (re_ottaa2,  u"ö",   u"öi",  u"Ammottaa",   u"Ammottaa"),

  (re_toninen, u"toni", u"tooni"),
  (re_iivinen, u"iivi", u"ivi"),
  (re_aalinen, u"aali", u"ali"),

  (re_nuolaista, u"Nuolaista_"),
  (re_rangaista, u"Rangaista_"),

  (re_eikAs, u"eik", u"ehik"),
]


def word_class (line):
    L = dict ([(u"[Ll]",  u"Laatusana"),
               (u"[Ln]",  u"Nimisana"),
               (u"[Lnl]", u"NimiLaatusana")])
    return L[line[0:line.find("]")+1]]


# Sanoja, joilla on vain muutama vanha taivutusmuoto. Generoidaan ne erikseen,
# mutta vain sanoille, jotka ovat Joukahaisessa. Sanat ovat Nykysuomen
# sanakirjan taivutuskaavojen numeroiden mukaisessa järjestyksessä.
#
# Tuomo Tuomi: Suomen kielen käänteissanakirja, 2. painos.
# Suomalaisen Kirjallisuuden Seura 1980.

def write_word (line, word, lexicon):
    prefix = line[0:line.find (u" ")]
    A = u"a" if re_A.search(word) else u"ä"
    outfile.write (u"%s %s%s_%s ;\n" % (prefix, word_class(line), lexicon, A))

def write_ahven (line, word):
    if not line.startswith (u"[Lu]"):
        write_word (line, word, u"SukijaAhven")

def write_kaunis (line, word):
    write_word (line, word, u"SukijaKaunis")

def write_altis (line, word):
    write_word (line, word, u"SukijaAltis")

def write_virkkaa (line, word):
    prefix = line[0:line.find (u" ")]
    outfile.write (u"%s SukijaVirkkaa_ä ;\n" % (prefix))

def write_paistaa (line, word):
    prefix = line[0:line.find (u" ")]
    outfile.write (u"%s SukijaPaistaa_a ;\n" % (prefix))

def write_paahtaa (line, word):
    prefix = line[0:line.find (u" ")]
    outfile.write (u"%s SukijaPaahtaa_a ;\n" % (prefix))

def write_lahti (line, word):
    write_word (line, word, u"SukijaLahti")


def generate_from_pattern_1 (line, pattern_list):
    for x in pattern_list:
        if x[0].match(line):
            if (len(x) == 2):
                outfile.write (line.replace (x[1], u"Sukija" + x[1]))
            elif (len(x) == 3) or (len(x) == 4 and not x[3].match(line)):
                replace_and_write (line, x[1], x[2])
            elif (len(x) == 5) and (line.find (x[3]) >= 0):
                replace_and_write (line.replace(x[3],x[4]), x[1], x[2])


def generate_from_pattern_2 (line, pattern, string, p1, p2, s1, s2):
    if pattern.match (line):
        for x in p1:
            replace_and_write (line, string, x)
        for x in p2:
            replace_and_write (line.replace(s1,s2), string, x)


# Old spellings and common spelling errors of words
# that do not conform to any pattern.
#
#    (u"", (u"", u"")),
#
word_list = [
    (u"aarteisto",        (u"aarteisto",     u"aartehisto")),
    (u"Abessinia",        (u"Abessini",      u"Abessiini", u"Abyssini", "Abyssiini")),
    (u"agaave",           (u"agaave",        u"agave")),
    (u"aggressiivinen",   (u"aggressiivi",   u"agressiivi", u"akressiivi")),
    (u"aggressio",        (u"aggressio",     u"agressio")),
    (u"aikainen",         (u"aikai",         u"aikahi")),
    (u"ainainen",         (u"ainai",         u"ainahi")),
    (u"aineisto",         (u"aineisto",      u"ainehisto")),
    (u"aksiomi",          (u"aksiom",        u"aksioom")),
    (u"aksiooma",         (u"aksioom",       u"aksiom")),
    (u"alamainen",        (u"alamai",        u"alammai")),
    (u"alimmainen",       (u"alimmai",       u"alimai")),
    (u"alkovi",           (u"alkov",         u"alkoov")),
    (u"ameba",            (u"ameb",          u"ameeb")),
    (u"amfiteatteri",     (u"amfiteatter",   u"amfiiteaatter", u"amfiteaatter")),
    (u"apassi",           (u"apass",         u"apash")),
    (u"apteekkari",       (u"apteekkar",     u"apteekar", u"aptekar")),
    (u"arsenikki",        (u"arsenik",       u"arseniik")),
    (u"assistentti",      (u"assistent",     u"asistent")),
    (u"Australia",        (u"Australi",      u"Austraali")),
    (u"barbaari",         (u"barbaar",       u"barbar")),
    (u"beduiini",         (u"beduiin",       u"beduin")),
    (u"biljardi",         (u"biljard",       u"biljaard")),
    (u"borssi",           (u"borss",         u"borsh")),
    (u"dervissi",         (u"derviss",       u"dervish", u"dervisch")),
    (u"diadeemi",         (u"diadeem",       u"diadem")),
    (u"divaani",          (u"divaan",        u"divan")),
    (u"drakma",           (u"drakm",         u"drakhm")),
    (u"edes",             (u"edes",          u"ees")),
    (u"emali",            (u"emal",          u"emalj")),
    (u"emaloida",         (u"emalo",         u"emaljo")),
    (u"embleemi",         (u"embleem",       u"emblem")),
    (u"ensimmäinen",      (u"ensimmäi",      u"ensimäi")),
    (u"eteinen",          (u"etei",          u"etehi")),
    (u"evankelinen",      (u"evankeli",      u"evankeeli")),
    (u"germaani",         (u"germaan",       u"german")),
    (u"haupitsi",         (u"haupits",       u"haubits")),
    (u"hevonen",          (u"hevo",          u"hevoi")),
    (u"humaaninen",       (u"humaani",       u"humani")),
    (u"husaari",          (u"husaar",        u"husar")),
    (u"huumori",          (u"huumor",        u"humor")),
    (u"inhimillinen",     (u"inhimilli",     u"inhimmilli")),
    (u"inkvisiittori",    (u"inkvisiittor",  u"inkvisitor", u"inkvisiitor")),
    (u"inkvisitio",       (u"inkvisitio",    u"inkvisiitio")),
    (u"insinööri",        (u"insinöör",      u"insinör")),
    (u"invalidi",         (u"invalid",       u"invaliid")),
    (u"janitsaari",       (u"janitsaar",     u"janitsar", u"janitschar", u"janitschaar", u"janitshaar")),
    (u"juridinen",        (u"juridi",        u"juriidi")),
    (u"kahdeksainen",        (u"kahdeksai",         u"kaheksai")),
    (u"kahdeksan",           (u"kahdeks",           u"kaheks")),
    (u"kahdeksankymppinen",  (u"kahdeksankymppi",   u"kaheksankymppi")),
    (u"kahdeksankertaistaa", (u"kahdeksankertaist", u"kaheksankertaist")),
    (u"kahdeksankymmen",     (u"kahdeksankymmen",   u"kaheksankymmen")),
    (u"kahdeksanlainen",     (u"kahdeksanlai",      u"kaheksanlai")),
    (u"kahdeksannes",        (u"kahdeksanne",       u"kaheksanne")),
    (u"kahdeksas",           (u"kahdeksa",          u"kaheksa")),
    (u"kaleeri",        (u"kaleer",      u"kaler")),
    (u"kamari",         (u"kamar",       u"kammar")),
    (u"kameli",         (u"kamel",       u"kameel")),
    (u"kamiina",        (u"kamiin",      u"kamin")),
    (u"kampanja",       (u"kampanj",     u"kamppanj")),
    (u"kaneli",         (u"kanel",       u"kaneel")),
    (u"kanuuna",        (u"kanuun",      u"kanun")),
    (u"kaoottinen",     (u"kaootti",     u"kaaootti", u"kaaotti", u"kaotti")),
    (u"kauan",          ((u"kauaa",      u"kauvaa"),
                         (u"kauan",      u"kauvan"),
                         (u"kauemmin",   u"kauvemmin"),
                         (u"kauimmin",   u"kauvimmin"))),
    (u"kauempi",        (u"kaue",        u"kauve")),
    (u"Kaukasia",       (u"Kaukasi",     u"Kaukaasi")),
    (u"kaunoinen",      (u"kaunoi",      u"kaunohi")),
    (u"katolilainen",   (u"katolilai",   u"katoolilai")),
    (u"katolinen",      (u"katoli",      u"katooli")),
    (u"kavaljeeri",     (u"kavaljeer",   u"kavalier", u"kavaljier")),
    (u"kenraali",       (u"kenraal",     u"kenral")),
    (u"kerubi",         (u"kerub",       u"keruub", u"kheruub")),
    (u"keskimmäinen",   (u"keskimmäi",   u"keskimäi")),
    (u"kirjoitelma",    (u"kirjoitelm",  u"kirjotelm")),
    (u"kollega",        (u"kolleg",      u"kolleg")),
    (u"kollegio",       (u"kollegio",    u"kolleegio")),
    (u"koneisto",       (u"koneisto",    u"konehisto")),
    (u"konossementti",  (u"konossement", u"konnossement")),
    (u"konttori",       (u"konttor",     u"kontoor")),
    (u"korsteeni",      (u"korsteen",    u"korstein")),
    (u"kortteeri",      (u"kortteer",    u"kortter", u"kortier", u"korttier")),
    (u"kraatteri",      (u"kraatter",    u"kraater", u"krateer")),
    (u"kritiikki",      ((u"kritiik",    u"kritik", u"NimisanaTakki_ä", u"NimisanaRisti_ä"),
                         (u"kritiik",    u"kriitiik"))),
    (u"kulttuuri",      (u"kulttuur",    u"kultuur", "kulttur")),
    (u"kuriiri",        (u"kuriir",      u"kurier")),
    (u"kurtiini",       (u"kurtiin",     u"kurtin")),
    (u"kuvernööri",     (u"kuvernöör",   u"kuvernör")),
    (u"Kööpenhamina",   (u"kööpenhamin", u"köpenhamin")),
    (u"laboratorio",    (u"laboratorio", u"laboratoorio")),
    (u"lauantai",       (u"lauanta",     u"lauvanta")),
    (u"lauantaisin",    (u"lauantaisin", u"lauvantaisin")),
    (u"leegio",         (u"leegio",      u"legio")),
    (u"legioona",       (u"legioon",     u"legion")),
    (u"legioonalainen", (u"legioonalai", u"legionalai")),
    (u"lestadiolainen", (u"lestadiolai", u"lestaadiolai", u"laestadiolai")),
    (u"liipaisin",      (u"liipaisi",    u"liipasi")),
    (u"likimmäinen",    (u"likimmäi",    u"likimäi")),
    (u"lordi",          (u"lord",        u"loord")),
    (u"luterilainen",   (u"luterilai",   u"lutherilai", u"luteerilai")),
    (u"lähimmäinen",    (u"lähimmäi",    u"lähimäi")),
    (u"majoneesi",      (u"majonees",    u"majonnees")),
    (u"majuri",         (u"majur",       u"majuur")),
    (u"mansetti",       (u"manset",      u"manshet")),
    (u"matrikkeli",     (u"matrikkel",   u"matrikel")),
    (u"mieluinen",      (u"mielui",      u"mieluhi")),
    (u"minareetti",     (u"minareet",    u"minaret")),
    (u"modeemi",        (u"modeem",      u"modem")),
    (u"moduuli",        (u"moduul",      u"modul")),
    (u"mosaiikki",      (u"mosaiik",     u"mosaik")),
    (u"muhamettilainen", (u"muhamettilai", u"muhammettilai", u"mahomettilai", u"muhamedilai")),
    (u"musiikki",        (u"musiik",      u"musik")),
    (u"Nubia",           (u"nubi",        u"nuubi")),
    (u"odottaa",         (u"odot",        u"oot")),
    (u"paitsi",          (u"paitsi",      u"paitse")),
    (u"paneeli",         (u"paneel",      u"panel")),
    (u"paratiisi",       (u"paratiis",    u"paradiis", u"paradis")),
    (u"parhaisto",       (u"parhaisto",   u"parahisto")),
    (u"paronitar",       (u"paronit",     u"paroonit")),
    (u"pasuuna",         (u"pasuun",      u"pasun")),
    (u"pataljoona",      (u"pataljoon",   u"pataljon")),
    (u"patriisi",        (u"patriis",     u"patris")),
    (u"patruuna",        (u"patruun",     u"patrun")),
    (u"perimmäinen",     (u"perimmäi",    u"perimäi")),
    (u"persoona",        (u"persoon",     u"person")),
    (u"piispa",          (u"piisp",       u"pisp")),
    (u"pioneeri",        (u"pioneer",     u"pioner")),
    (u"pioni",           (u"pion",        u"pioon")),
    (u"pitaali",         (u"pitaal",      u"pital")),
    (u"plebeiji",        (u"plebeij",     u"plebej")),
    (u"plutoona",        (u"plutoon",     u"pluton")),
    (u"poliisi",         (u"poliis",      u"polis")),
    (u"poliitikko",      (u"poliitik",    u"politik", u"poliitiik")),
    (u"poliittinen",     (u"poliitti",    u"politti", u"poliittii")),
    (u"politiikka",      (u"politiik",    u"politik", u"poliitiik")),
    (u"Polynesia",       (u"Polynesi",    u"Polyneesi")),
    (u"posetiivi",       (u"posetiiv",    u"posetiv")),
    (u"positiivi",       (u"positiiv",    u"positiv")),
    (u"posliini",        (u"posliin",     u"poslin"   u"porsliin", u"porslin")),
    (u"preettori",       (u"preettor",    u"preetor", u"pretor")),
    (u"pretoriaani",     (u"pretoriaan",  u"pretorian")),
    (u"probleemi",       (u"probleem",    u"problem")),
    (u"pudottaa",        (u"pudo",        u"puo")),
    (u"pyramidi",        (u"pyramid",     u"pyramiid")),
    (u"päällimmäinen",   (u"päällimmäi",  u"päällimäi", u"päälimäi", u"päälimmäi")),
    (u"päärynä",         ((u"pääryn", u"pääron", u"NimisanaPeruna_ä", u"NimisanaPeruna_aä"), )),
    (u"rangaistus",      (u"rangaistu",   u"rankaistu")),
    (u"reettori",        (u"reettor",     u"reetor")),
    (u"reunimmainen",    (u"reunimmai",   u"reunimai")),
    (u"romanttinen",     (u"romantti",    u"romanti", u"romantilli")),
    (u"saippua",         (u"saippu",      u"saipu")),
    (u"samanlainen",     (u"samanlai",    u"samallai")),
    (u"samojedi",        (u"samojed",     u"samojeed")),
    (u"sampanja",        (u"sampanj",     u"samppanj")),
    (u"sankaruus",       (u"sankaruu",    u"sankariu")),
    (u"saraseeni",       (u"saraseen",    u"sarasen")),
    (u"sapatti",         (u"sapat",       u"sabat")),
    (u"sapeli",          (u"sapel",       u"sapeel")),
    (u"seminaari",       (u"seminaar",    u"seminar")),
    (u"senaatti",        ((u"senaat",     u"senaat", u"NimisanaTatti_a", u"NimisanaRisti_a"),
                          (u"senaat",     u"senat",  u"NimisanaTatti_a", u"NimisanaRisti_a"))),
    (u"senaattori",      (u"senaattor",   u"senaator")),
    (u"serafi",          (u"seraf",       u"seraaf")),
    (u"shampanja",       (u"shampanj",    u"shamppanj")),
    (u"sihteeri",        (u"sihteer",     u"sihter", u"sihtier")),
    (u"sikari",          (u"sikar",       u"sikaar")),
    (u"sitruuna",        (u"sitruun",     u"sitrun", u"sitroon", u"sitron")),
    (u"sitäpaitsi",      (u"paitsi",      u"paitse")),
    (u"siviili",         (u"siviil",      u"sivil")),
    (u"slaavilainen",    (u"slaavilai",   u"slavilai")),
    (u"soolo",           (u"soolo",       u"solo")),
    (u"soopeli",         (u"soopel",      u"sopel", u"soobel")),
    (u"spitaali",        (u"spitaal",     u"spital")),
    (u"stationaarinen",  ((u"stationaari", u"stationääri", u"LaatusanaNainenInen_a ", u"LaatusanaNainenInen_ä"), )),
    (u"synagoga",        (u"synagog",      u"synagoog")),
    (u"taimmainen",      (u"taimmai",      u"takimai", u"taemmai", u"taaemmai")),
    (u"tantieemi",       (u"tantieem",     u"tantiem")),
    (u"teatteri",        (u"teatter",      u"teaater", u"teaatter", u"teater")),
    (u"temperamentti",   (u"temperament",  u"tempperament")),
    (u"tooga",           (u"toog",         u"tog")),
    (u"topaasi",         (u"topaas",       u"topas")),
    (u"Toscana",         (u"toscan",       u"toskan")),
    (u"toteemi",         (u"toteem",       u"totem")),
    (u"torpedo",         (u"torpedo",      u"torpeedo")),
    (u"Traakia",         (u"Traaki",       u"Traki")),
    (u"traakialainen",   (u"traakialai",   u"trakialai")),
    (u"tussi",           (u"tuss",         u"tush")),
    (u"tällainen",       ((u"tällai",      u"tällai", u"NimiLaatusanaNainenInen_a", u"NimiLaatusanaNainenInen_ä"),
                          (u"tällai",      u"tälläi", u"NimiLaatusanaNainenInen_a", u"NimiLaatusanaNainenInen_ä"),
                          (u"tällai",      u"tälläi", u"NimiLaatusanaNainenInen_a", u"NimiLaatusanaNainenInen_a"))),
    (u"ulommainen",      (u"ulommai",      u"uloimmai")),
    (u"upseeri",         (u"upseer",       u"upser", u"upsier")),
    (u"upseeristo",      (u"upseeristo",   u"upsieristo")),
    (u"vasemisto",       (u"vasemisto",    u"vasemmisto")),
    (u"viheriöidä",      (u"viheriö",      u"viherjö")),
    (u"vihkiäinen",      (u"vihkiäi",      u"vihkijäi")),
    (u"yhdeksäinen",        (u"yhdeksäi",         u"yheksäi")),
    (u"yhdeksän",           (u"yhdeks",           u"yheks")),
    (u"yhdeksänkymppinen",  (u"yhdeksänkymppi",   u"yheksänkymppi")),
    (u"yhdeksänkertaistaa", (u"yhdeksänkertaist", u"yheksänkertaist")),
    (u"yhdeksänkymmen",     (u"yhdeksänkymmen",   u"yheksänkymmen")),
    (u"yhdeksänlainen",     (u"yhdeksänlai",      u"yheksänlai")),
    (u"yhdeksännes",        (u"yhdeksänne",       u"yheksänne")),
    (u"yhdeksäs",           (u"yhdeksä",          u"yheksä")),
    (u"ylimmäinen",         (u"ylimmäi",          u"ylimäi")),

    (u"ien",     [u"[Ln][Xp]ien[X]iken[Sn][Ny]e:ikene Loppu ;",
                  u"[Ln][Xp]ien[X]ien[Ses][Ny]nä:iennä NimisanaLiOlV_ä ;"]),

    (u"kappale", [u"[Ln][Xp]kappale[X]kappal[Sg][Nm]ten:kappalten # ;"]),
    (u"maailma", [u"[Ln][Xp]maailma[X]maailmoitse:maailmoitse # ;"]),
    (u"pieni",   [u"[Ll][Xp]pieni[X]pien[Ses][Ny]nä:piennä NimisanaLiOlV_ä ;"]),
    (u"sankari", [u"[Ln][Xp]sankari[X]sankar[Sg][Nm]ten:sankarten # ;"]),
    (u"tuta",    [u"[Lt][Xp]tuta[X]tu:tu SukijaTuta ;"]),
    (u"venäjä",  [u"[Ln][Xp]venäjä[X]venä[Sp][Ny]ttä:venättä NimisanaLiOlV_ä ;"]),

    (u"lainen",  lambda line, word: replace_and_write (line.replace(u"lai",u"läi"), u"NimiLaatusanaNainen_a", u"NimiLaatusanaNainen_ä")),

    # 39 nuori (3, 3). Tuomi, s. 182, 184.
    #
    (u"juuri",   [u"[Ln][Xp]juuri[X]juur[Ses][Ny]na:juurna NimisanaLiOlV_a ;",
                  u"[Ln][Xp]juuri[X]juur[Ses][Ny]ra:juurra NimisanaLiOlV_a ;"]),
    (u"nuori",   [u"[Lnl][Xp]nuori[X]nuor[Ses][Ny]na:nuorna NimisanaLiOlV_a ;",
                  u"[Lnl][Xp]nuori[X]nuor[Ses][Ny]ra:nuorra NimisanaLiOlV_a ;"]),
    (u"suuri",   [u"[Lnl][Xp]suuri[X]suur[Ses][Ny]na:suurna NimisanaLiOlV_a ;",
                  u"[Lnl][Xp]suuri[X]suur[Ses][Ny]ra:suurra NimisanaLiOlV_a ;"]),

    # 46 hapsi (1, 1). Tuomi, s. 190. -- Vvfst tunnistaa muodot "hasten" ja "hapsien".
    # hasna, hassa, hasten, hapsien   -- Nämä ovat niin harvinaisia, että tarvitseeko näitä indeksoinnissa?
    #
#    (u"hapsi", [u"[Ln][Xp]hapsi[X]has[Ses][Ny]na:hasna NimisanaLiOlV_a ;",
#                u"[Ln][Xp]hapsi[X]has[Ses][Ny]sa:hassa NimisanaLiOlV_a ;"]),

    # 78 hame
    #
    (u"hame",  [u"[Ln][Xp]hame[X]hame[Sp][Ny]hta:hamehta NimisanaLiOlV_a ;"]),

    # 79 terve (4, 4). Tuomi s. 142, 143, 146.
    #
    (u"tuore", [u"[Ll][Xp]tuore[X]tuore[Ses][Ny]nna:tuorenna NimisanaLiOlV_a ;"]),
    (u"vetre", [u"[Ll][Xp]vetre[X]vetre[Ses][Ny]nnä:vetrennä NimisanaLiOlV_ä ;"]),
    (u"päre",  [u"[Ln][Xp]päre[X]päre[Ses][Ny]nnä:pärennä NimisanaLiOlV_ä ;"]),
    (u"terve", [u"[Lnl][Xp]terve[X]terve[Ses][Ny]nnä:tervennä NimisanaLiOlV_ä ;"]),

    (u"kaivu", [u"[Ln][Xp]kaivu[X]kaivu:kaivu NimisanaPuu_a ;",
                u"[Ln][Xp]kaivu[X]kaivu[Sill][Ny]usee:kaivuusee NimisanaLiOlN_a ;"]),
]


function_list = [
    # Herttua-tyyppisillä sanoilla on monikkomuodot, joissa ei ole o:ta (herttuilla, jne).
    #
    # 20 herttua (10, 10). Tuomi, s. 114, 116, 121, 124, 125.
    #
    (lambda line, word: outfile.write (u"[Ln][Xp]%s[X]%s:%s SukijaHerttua ;\n" %
                                       (word, word[0:len(word)-1], word[0:len(word)-1])),
     (u"aurtua",
      u"herttua",
      u"hierua",
      u"juolua",
      u"lastua",
      u"liettua",
      u"luusua",
      u"porstua",
      u"saarua",
      u"tanhua")),

# Vapaa ja tienoo ovat taivutuskaavoina SukijaVapaa.
#
    # 23 vapaa (8, 8). Tuomi, s. 1, 2.
    #
#    (write_vapaa_tienoo,
#     (u"kajaa",
#      u"vajaa",
#      u"vakaa",
#      u"suklaa",
#      u"harmaa",
#      u"vapaa",
#      u"nepaa",
#      u"hurraa")),

    # 24 tienoo (14, 14). Tuomi, s. 345. Taipuu kuten vapaa.
    #
#    (write_vapaa_tienoo,
#     (u"kabeljoo",
#      u"kalikoo",
#      u"pikoo",
#      u"talkoo",
#      u"haloo",
#      u"halloo",
#      u"tienoo",
#      u"poppoo",
#      u"bigarroo",
#      u"platoo",
#      u"ehtoo",
#      u"palttoo",
#      u"ponttoo",
#      u"nivoo")),

    # 33 lohi (2, 2). Tuomi, s. 151.
    # lohten, uuhten
    #
    (lambda line, word: outfile.write (u"[Ln][Xp]%s[X]%s:%s SukijaLohi ;\n" %
                                       (word, word[0:len(word)-1], word[0:len(word)-1])),
     (u"lohi",
      u"tyynenmerenlohi",   # On Joukahaisessa.
      u"uuhi")),

    # 34 lahti (2, 2). Tuomi, s. 193.
    # lahta (= lahtea), lahtein
    #
    (write_lahti, 
     (u"haahti",
      u"lahti")),

    # Ahven taipuu kuten sisar, paitsi että yksikön olento on myös ahvenna.
    #
    # 55 ahven (22, 23). Tuomi, s. 246, 247, 301, 302.
    #
    (write_ahven,
     (u"aamen",
      u"ahven",
      u"haiven",
      u"huomen",
      u"häiven",
      u"höyhen",
#      u"ien",  # On erikseen: ikene, ien.
      u"iljen",
      u"joutsen",
      u"jäsen",
      u"kymmen",
      u"kämmen",
      u"liemen",
      u"paimen",
      u"siemen",
      u"ruumen",
      u"terhen",
      u"taimen",
      u"tuumen",
      u"tyven",
      u"tyyven",
      u"uumen",
      u"vuomen")),

    # 69 kaunis (7, 6). Tuomi, s. 358.
    #
    (write_kaunis,
     (u"kallis",
      u"aulis",
      u"valmis",
      u"kaunis",
#      u"altis",
      u"tiivis")),

     (write_altis, (u"altis", )),

     # 11 paistaa (9, 9). Tuomi s. 1, 2, 8, 11, 12, 15, 17.
     #
     (write_virkkaa, (u"vilkkaa",
                      u"virkkaa")),
     (write_paistaa, (u"paistaa", )),
     (write_paahtaa, (u"paahtaa",
                      u"raistaa",
                      u"saattaa",
                      u"taittaa",
                      u"palttaa",
                      u"varttaa")),
     (lambda line, word: outfile.write (line.replace (u"NimisanaVati_ä", u"SukijaNeiti")),
       (u"neiti")),
]

def convert_to_dictionary (word_list):
    l0 = map (lambda x : x[0], word_list)
    l1 = map (lambda x : x[1], word_list)
    return dict (zip (l0, l1))

sukija_dictionary = convert_to_dictionary (word_list)


def error (line):
    sys.stderr.write (line)
    sys.stderr.write ("Wrong format in sukija_dictionary.\n")
    sys.exit (1)


def write_list (line, key, data):
    for x in data:
        if type(x) == UnicodeType:
            outfile.write (x + u"\n")
        else:
            error (line)


def write_tuple (line, key, g):
     if type(g[0]) == UnicodeType:
         for i in range (1, len(g)):
             replace_and_write (line, g[0], g[i])
     elif type(g[0]) == TupleType:
         for i in range (0, len(g)):
             if (len(g[i]) == 2):
                 replace_and_write (line, g[i][0], g[i][1])
             else:
                 s = line.replace (g[i][2], g[i][3])
                 outfile.write (replace (s, g[i][0], g[i][1]))
     else:
         error (line)


# Extract base form from a line.
#
base_form_re = re.compile (u"\\[Xp\\]([^[]+)\\[X\\]", re.UNICODE)

def generate_word (r, line, sukija_dictionary):
    try:
        g = sukija_dictionary[r.group(1)]
        if type(g) == ListType:
            write_list (line, r.group(1), g)
	elif type(g) == TupleType:
            write_tuple (line, r.group(1), g)
	elif type(g) == LambdaType:
            g (line, r.group(1))
	else:
            error (line)
    except KeyError:  # It is not an error if a word is not in sukija_dictionary.
        pass


def generate_from_function (r, line, function_list):
    for x in function_list:
        if r.group(1) in x[1]:
            x[0] (line, r.group(1))


def generate_xiljoona (line):
    if (line.startswith ("[Sn]")):
        u = line.replace (u"miljoona@", u"miljona@")
        u = u.replace (u"miljoonat@", u"miljonat@")
        u = u.replace (u"biljoona@",  u"biljona@")
        u = u.replace (u"biljoonat@", u"biljonat@")
        u = u.replace (u"triljoona@",  u"triljona@")
        u = u.replace (u"triljoonat@", u"triljonat@")
        outfile.write (u)
    else:
        outfile.write (line.replace (u"iljoon", u"iljon"))
        if (line.startswith (u"@") and line.find (u"iljoonien:")):
            outfile.write (line.replace (u"iljoonien", u"iljoonain"))
            outfile.write (line.replace (u"iljoonien", u"iljonain"))


ei_vertm = re.compile (u"@[PDC][.]EI_VERTM([.]ON)?@", re.UNICODE)


sukija_additions = {
    u"LEXICON Sanasto\n":       u"Sukija ;\nSukijaSuhdesana ;\n",
    u"LEXICON Sanasto_p\n":     u"Sukija_p ;\n",
    u"LEXICON Sanasto_em\n":    u"SukijaPoikkeavat_em ;\n",
    u"LEXICON Sanasto_ep\n":    u"SukijaPoikkeavat_ep ;\n",
    u"LEXICON LukusananErikoisjälkiliite\n": u"SukijaLukusananErikoisjälkiliite ;\n",
    u"LEXICON Omistusliite_a\n":  u"[O2y]s:s      Liitesana_a     ;\n",
    u"LEXICON Omistusliite_ä\n":  u"[O2y]s:s      Liitesana_ä     ;\n",
    u"LEXICON Omistusliite_aä\n": u"[O2y]s:s      Liitesana_aä    ;\n"
}


def write_sukija_additions (line, sukija_additions):
    try:
        outfile.write (sukija_additions[line])
    except KeyError:
        pass


# Copy Voikko vocabulary and insert forms that Sukija needs.
#
while True:
    line = infile.readline()
    if line == u"":
        break
    line = re.sub (ei_vertm, u"", line)
    if OPTIONS["sukija-ys"]:
        line = line.replace (u"@P.YS_EI_JATKOA.ON@" , u"")
        line = line.replace (u"@D.YS_EI_JATKOA@", u"")
        line = line.replace (u"@C.YS_EI_JATKOA@", u"")
    outfile.write (line)
    write_sukija_additions (line, sukija_additions)

    generate_from_pattern_1 (line, spelling_pattern_list)

    generate_from_pattern_2 (line, re_uusio, u"uusio", (u"usio",),          (u"usion",  u"usioon"),  u"NimisanaAutio_a", u"NimisanaPaperi_a")
    generate_from_pattern_2 (line, re_tio,   u"tio",   (u"tsio",),          (u"tsion",  u"tsioon"),  u"NimisanaAutio_a", u"NimisanaPaperi_a")
    generate_from_pattern_2 (line, re_aatio, u"aatio", (u"atio", u"atsio"), (u"atsion", u"atsioon"), u"NimisanaAutio_a", u"NimisanaPaperi_a")
    generate_from_pattern_2 (line, re_uutio, u"uutio", (u"utio", u"utsio"), (u"utsion", u"utsioon"), u"NimisanaAutio_a", u"NimisanaPaperi_a")


    r = base_form_re.search (line)
    if r:
        generate_word (r, line, sukija_dictionary)
        generate_from_function (r, line, function_list)
    if (re_Xiljoona.search (line)):
        generate_xiljoona (line)
infile.close()

outfile.write (u"\n\n\n")

while True:
    line = sukijafile.readline()
    if line == u"":
        break
    outfile.write (line)
sukijafile.close()

outfile.close()
