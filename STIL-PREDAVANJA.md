# Stil i izrada predavanja

Programiranje za web, SIT UNIZD. Dokument opisuje kako su složena predavanja u ovom
repozitoriju i što treba provjeriti prije nego se predavanje proglasi gotovim.
Nije popis preporuka nego popis pravila koja su nastala ispravljanjem konkretnih
slajdova, pa svako od njih ima iza sebe primjer koji nije prošao.

Dizajn je ovdje sporedan. Riječ je o sadržaju, didaktičkom redoslijedu i jeziku.

Cjeline 1 do 13 su pravila. Cjeline 14 do 20 su izvedba: obrazac slajdova, preambula,
prijevod i provjera, mjere za prijelom, zamke u LaTeXu, provjera uz kod referentnog
projekta i trenutni raspored gradiva po terminima.

Uz dokument ide prevediv primjer svakog oblika slajda, `Predavanja/obrazac/obrazac.tex`.
Tko mijenja predavanje, otvara njega uz ovaj popis. Sve putanje u ovom dokumentu
navedene su u odnosu na korijen repozitorija predavanja.

---

## 1. Što predavanje jest

Predmet je razvoj web aplikacija. Referentna aplikacija je ilustracija, nikada tema.
Slajd koji nabraja rute, polja ili nazive vrijednosti iz referentne aplikacije ondje
gdje one nisu gradivo pretvara predavanje u dokumentaciju jednog projekta.

Ilustracija se piše riječima: „klub prijavljuje natjecatelja", a ne „`POST
/competitions/{id}/registrations` vraća `201`". Iznimka je slajd kojemu su rute,
polja ili kodovi sami predmet.

Kad domenski detalj ipak treba, označava se kao izbor ovog projekta, a ne kao pravilo
struke.

### Jedan do dva ishoda po predavanju

Student iz predavanja iznosi jedan do dva ishoda. Predavanje koje nabraja desetak
jednako važnih stvari nije bogato nego pretrpano, a na kraju se ne pamti nijedna.

Kad se bira što izbaciti, ostaje ono što nosi ishod. Gradivo koje je točno, ali ne
služi ishodu toga tjedna, seli u tjedan kojemu služi ili izlazi.

---

## 2. Didaktički redoslijed

### Problem pa rješenje, uvijek

Redoslijed unutar svakog slajda i svake cjeline: prvo opasnost ili problem, pa tek
onda sredstvo koje ga uklanja.

Krivo: „`order_by` nam treba jer bez njega straničenje ne radi."

Ispravno: „Straničenje bez izrijekom zadanog poretka ne radi ispravno, jer ga baza
sama ne jamči. Bez `order_by` isti zapis može doći i na prvu i na drugu stranicu, a
drugi zapis ni na jednu."

Slajd zbog toga smije postati gušći. Gustoća je prihvatljiva cijena, obrnut redoslijed
nije.

### Problem mora biti vidljiv, ne samo tvrđen

Nije dovoljno reći da problem postoji. Student mora imati za što se uhvatiti: poruku
pogreške, ispis dnevnika, dva broja koja se razlikuju, dva zahtjeva jedan uz drugi.
Problem koji se samo tvrdi student ne prepozna kao problem, pa ni rješenje ne shvati
kao rješenje.

Red je: pokazati kvar, imenovati ga, pokazati zahvat koji ga uklanja, reći što taj
zahvat košta.

### Problem i rješenje su dva slajda

Slajd koji iznese problem i odmah ga riješi prekratko je stao na problemu. Jedan slajd
postavlja pitanje, sljedeći odgovara. Između njih predavač pita razred.

### Pokazati prije nego se o tome govori

Ne raspravljati o dijelovima nečega što student nije vidio. Token se prvo ispiše cijel,
s oznakama koji je dio koji, pa se tek onda govori o potpisu. Inače „usporedi se s
priloženim potpisom" nema na što pokazati. Isto vrijedi za zahtjev, odgovor, migraciju
i strukturu mapa.

### Jedan novi pojam po slajdu

Dijagram ili tablica koja uvodi četiri nova naziva odjednom ne objašnjava ništa. Prije
uporabe pojma provjeriti je li igdje definiran. Kad se nešto uvodi, veže se na već
poznate pojmove i na kod koji je na zaslonu, ne na novo nazivlje.

### Opći pojam dobiva primjer izvan domene kolegija

Kad slajd uvodi pojam struke, primjer dolazi izvan domene referentne aplikacije:
prava nad datotekom u operacijskom sustavu, uredništvo portala, pristup dokumentu u
ustanovi. Tek zaključna rečenica ili tablica kaže što projekt koristi.

Razlog je praktičan: s domenskim primjerom izgleda kao da projekt mijenja model čim se
pojavi novo pravilo, a ne mijenja ga.

---

## 3. Struktura

Plan predavanja, Ishodi učenja, Domena primjera, cjeline, Sažetak.

Cjelina se otvara razdjelnikom: naslov cjeline i jedna linija koja nabraja njezine
teme. Cjelina s jednim ili dva slajda nije cjelina; spaja se ili proširuje.

Sažetak je točno jedan, na kraju. Bez završnih misli i bez slajda „Pitanja?".

### Predavanje je samostalno

Student koji je propustio prošli tjedan mora moći pratiti.

Druga predavanja se ne spominju: ni unaprijed ni unatrag, ni brojem ni imenom.
„Takva su pravila tema šestoga predavanja" i „kao što smo vidjeli prošli tjedan"
oboje izlaze.

Gradivo ranijeg predavanja koje trenutnom treba podsjeća se jednom rečenicom na mjestu
uporabe, s onoliko sadržaja koliko je za taj korak potrebno: „Statusni kod `422` znači
da tijelo ne odgovara shemi." Pozivanje na raniju razliku kao na poznatu ne vrijedi;
razliku između `400` i `422` studenti ne znaju napamet.

### Isti slajd ne stoji u dvama predavanjima

Kad se gradivo mora ponoviti, ponavlja se u jednoj rečenici na mjestu uporabe ili kao
izrijekom označen podsjetnik, nikad kao ponovljeno izlaganje.

### Što nije gradivo

Sadržaj o metodi izvođenja nastave nije gradivo: popis commitova predavanja, upute kako
gledati razlike, najava sljedećeg predavanja, najava vježbi. Ili se pretvara u temu
struke ili izlazi.

Na slajd ne ide ni ono što predavač izvodi uživo: mjerenje vremena petljom, pokretanje
skripte koja nešto broji, koraci u alatu. Slajd nosi kod i, kad je poučan, ispis koji
iz njega slijedi.

---

## 4. Naslovi

Naslov slajda je trijezna imenska fraza koja imenuje sadržaj: „Granica odluke",
„Mjesto poslovnog pravila", „Vijek tokena". Kad se tema dijeli, naslov ostaje isti uz
oznake `(I)` i `(II)`.

Zabranjeni obrasci:

| Obrazac | Primjer | Umjesto toga |
|---|---|---|
| „A, ne B" | „Izbor, ne pravilo" | imenovati ono o čemu je riječ |
| broj kao naslov | „Tri faze", „Tri radnje, jedan put" | „Razdoblja natjecanja" |
| „zašto baš" | „Zašto baš Vue" | izbor ide u okvir za konvenciju |
| „X vs Y" | „Vite vs Webpack" | „X i Y" ili ime onoga što se uspoređuje |
| skrivena rečenica | „Gdje pravilo stoji" | „Mjesto poslovnog pravila" |
| odjeljak dokumentacije | „Česte greške početnika", „Konvencije i alati" | razlomiti po mjestima na koja sadržaj pripada |
| doskočica | „X na djelu", „X u našim rukama" | imenska fraza |

Naslov u obliku pitanja dolazi u obzir samo kad ga predavač izrijekom zatraži.

---

## 5. Jezik

Akademski registar, bez iznimke. Nikad kolokvijalno, nikad marketinški.

### Opće

- Red riječi je običan: subjekt, predikat, objekt. Bez inverzija i poetskog reda
  („Trajan ipak još nije", „Granica je time jasna").
- Bezlične konstrukcije ispred obraćanja: „ako je skupina nazvana X", ne „nazoveš li
  skupinu X". Pogodbena inverzija se uz to čita kao pitanje („Jesu li obje bez oznake,
  …"), pa ide „Ako su obje bez oznake, …".
- Bez prvog lica na slajdu („na obrani pitam", „tražim").
- **Bez em-crtice.** Umjesto nje dvotočje, zarez, zagrada ili nova rečenica.
- Rečenica bez subjekta nije rečenica: „Tri provjere nad tokenom" postaje „Nad tokenom
  radimo tri provjere".
- Broj stavki u popisu navodi se kad je sam broj dio gradiva. Ne navodi se kad je
  nečega slučajno toliko.
- Brojka koja se mijenja s kodom ne ide na slajd: broj testova, broj ruta, broj redaka.

### Figure koje odgovaraju na neizrečen prigovor

Brišu se: „nije ukras", „nije stvar ukusa", „time nisu iznimka", „nije X nego Y",
„nije prepreka". Nitko taj prigovor nije postavio.

### Kalkovi iz engleskog

Česti, i teško se primjećuju nakon nekoliko sati rada:

| Kalk | Umjesto |
|---|---|
| „strana sigurnosti" (*safe side*) | imenovati što se štiti |
| „razlika je u tome što se broji" (*what counts*) | imenovati ono što se uspoređuje |
| „vrijedi za" u značenju *applies to* | „primjenjuje se na", „obuhvaća", „ocjenjuje se" |
| „ovo doslovno radi" | izbaciti |
| „granica transakcije" | reći tko transakciju otvara i tko je zatvara |

### Poštapalice i prazni pojačivači

„higijena", „ključno", „upravo", „zapravo", „obavezno", „bez ikakvog popusta",
„pritom", „ipak", „stoga", „naime". U pravilu se brišu bez gubitka značenja.

### Anglizmi

Prvo pojavljivanje u predavanju ide u kurziv, uz hrvatski ekvivalent u zagradi ako
postoji i ako nije već udomaćen. Dalje običnim slogom. Nikad u naslovu i nikad u
citiranom kodu.

---

## 6. Nazivlje

Jedan pojam, jedna riječ, kroz cijeli kolegij. Kad se termin promijeni, promjena se
provodi kroz sve materijale, ne samo na mjestu primjedbe.

| Pojam | Na slajdu |
|---|---|
| backend, frontend | ostaju engleski; pri prvom spomenu hrvatski u zagradi |
| slojevi backenda | `routers`, `schemas`, `services`, `repositories`, i u slikama |
| framework | „framework", nikad „okvir" |
| projekt | ono što gradimo |
| API | vanjski ugovor prema klijentu |
| aplikacija | ponašanje cjeline |
| git | `commit`, `branch`, `remote`, `diff` na engleskom |
| zapisnik | jednom „zapisnik (engl. *log*)", dalje `logger`, `logging` |
| nositelj radnje | klub, a račun kluba kad je riječ baš o prijavi |
| uloga `admin` | organizator, jer je to njegov posao u domeni |
| salt, hash | engleski, ne „sol" i „otisak" |
| straničenje | ne „paginacija" |

Riječi koje se sudaraju i zato traže oprez:

- **repozitorij** u ovom kolegiju znači git repozitorij. Sloj pristupa bazi zove se
  sloj `repositories`, u kodnom slogu.
- **sjednica** je HTTP sjednica, **sesija** je sesija baze.
- **sučelje** je dvoznačno. Prema značenju: „API", „projekt", „aplikacija",
  „korisničko sučelje".

Prije uvođenja hrvatskog termina provjeriti nosi li već drugo tehničko značenje u
kurikulumu studija.

### Imenuj ono na što se pozivaš

Ne „odgovor o prijavi nosi i ime natjecatelja" nego „`RegistrationResponse` ima polje
`lifter`". Ne „sloj iznad nje" nego „sloj `services`". Ne „drugi zapis" ako prije toga
nije rečeno „jedan zapis".

---

## 7. Činjenica, konvencija, izbor

Tvrdnja na slajdu mora biti obranjiva uvijek, ne samo u ovom projektu. Studenti s
iskustvom prepoznaju pretjerivanje i time gube povjerenje u ostatak predavanja.

Sve što je dogovor struke ili odluka razvijatelja ide u zaseban okvir, odvojeno od
tvrdnji koje propisuje standard. U ovom repozitoriju za to služi okolina `konvencija`,
čiji se naslov mijenja prema prilici: „Konvencija", „Izbor, ne pravilo", „Razlikuje se
od projekta do projekta".

Ne hardkodirati tuđi ukus: inačica slike kontejnera, politika ponovnog pokretanja,
izbor `400` naspram `422`. Reći ono što je sigurno, ostalo označiti kao izbor.

Vrijednosti iz koda nisu apsolutne: ne „vrijedi petnaest minuta" nego „vrijedi kratko,
u ovom projektu petnaest minuta".

Kad se nabraja skup, popis mora biti potpun za kontekst ili izrijekom reći što
izostavlja i zašto.

Tvrdnja o tome što alat ne može provjerava se, ne pretpostavlja. Primjer greške: „tip
ne može nabrojiti dopuštene vrijednosti" za kategoriju. Može;
`Literal["83", "120+"]` radi s nizovima znakova. Stvarni je razlog bio drugi.

---

## 8. Kod na slajdu

### Isječak ima kontekst

Isječak koji počinje usred funkcije, bez potpisa i bez pozivatelja, ne pokazuje ništa.
Prikazuje se od potpisa funkcije, a ono što se izostavlja zamjenjuje se komentarom i
trotočjem, nikad prešućivanjem.

Kad slajd govori o odnosu dviju datoteka, obje se vide, svaka u svojem okviru, svaka s
putanjom u prvom retku.

### Kod odgovara tjednu i repozitoriju

Prije pisanja predavanja za tjedan N provjeriti u povijesti repozitorija kada koja
datoteka i koji pojam ulaze u projekt.

- Svaka putanja navedena na slajdu mora postojati u repozitoriju. Ako prirodno mjesto
  postoji, a kod ondje ne stoji, to se kaže u komentaru isječka.
- Smije se uvesti pojam, pa i kratak generički isječak, prije nego kod uđe u projekt.
  Greška je tek ulaziti u detalje mehanizma koji se objašnjava mnogo kasnije.
- Ne objašnjavati u tjednu N kod koji je ušao u tjednu N-1 kao da je nov. Ako se
  vraćamo na njega, reći izrijekom da se vraćamo i zašto baš sada.
- Razilaženje slajda i koda u sitnicama je dopušteno jer slajd uči teoriju. Nije
  dopuštena provjera koju datoteka nema, niti funkcija koja radi nešto drugo.
- Kod na slajdu mora odgovarati onome što tekst tvrdi. Ako tekst kaže „ovo je cijeli
  backend", kod mora vraćati podatke.

---

## 9. Grafika

Kad slajd prozom opisuje raspored nečega, taj se raspored crta.

Rečenica koja nabraja položaje, redoslijed ili pretvorbe opis je slike koja nedostaje:
„sljedeća su 22 znaka salt, a ostatak hash" je slika; ponašanje stupca pri upisu i
čitanju je tablica; put zahtjeva kroz slojeve je dijagram.

Vizual mora prikazivati pojavu, ne ukrašavati. Ako slajd tvrdi da nešto ne radi, na
slici se mora vidjeti kvar. Sve osi i oznake imenovane. Natuknica ne prepričava sliku
nego dodaje tumačenje.

---

## 10. Gustoća i prijelom

Slajd s tri odlomka i tablicom je dva slajda.

Kad slajd ne stane, dijeli se. **Tekst se ne krati zato da bi slajd stao.** Rečenica se
smije skratiti samo ako je i sama po sebi suvišna. Prvo sredstvo je prijelom na dva
slajda, drugo brisanje cijele suvišne tvrdnje, treće i zadnje preoblikovanje rečenice.

Smanjivanje fonta da bi sadržaj stao (`shrink` u Beameru) ne dolazi u obzir. Slajdovi
različite veličine slova unutar istog predavanja izgledaju neuredno, a pravi je problem
u tome što na slajdu ima previše sadržaja.

Nabrajanje od pet koraka su natuknice, ne rečenica s dvotočjem. Kad slajd nosi nekoliko
zasebnih tvrdnji, one moraju disati: razmak između odlomaka, ne tri odlomka zbijena
jedan na drugi.

Tablica je onoliko široka koliko joj sadržaj traži. Tablica razvučena preko cijele
širine s kratkim ćelijama i prelomljenim retcima izgleda loše, kao i uska tablica
centrirana usred praznog slajda dok odlomci idu punom širinom. Tablica se odvaja od
naslova razmakom.

Ne opisivati u natuknici ono što slika ili kod već pokazuju.

---

## 11. Vježbe

Vježba je slajd kao i svaki drugi i ima stalan oblik kroz sva predavanja. Student koji
je naučio čitati jednu vježbu mora moći čitati sve.

Oblik:

1. Uvodna rečenica koja postavlja ulogu, račun i polazno stanje. Lozinka se ne navodi.
2. Ako zadatak traži tijelo zahtjeva, ono stoji u isječku odmah iza uvoda, s
   prazninama ondje gdje vrijednost ovisi o stanju baze.
3. Numerirani koraci. Svaki korak je radnja, ne opis.
4. Jedna zaključna rečenica koja traži objašnjenje, ne potvrdu.

Pravila:

- **Ishod se ne piše.** „Odgovor je `422`" i „Ostala polja stoje" otkrivaju ono što
  student treba vidjeti sam.
- **Koraci su konkretni.** Ne „prijavite natjecatelja" nego koji natjecatelj, u kojoj
  kategoriji, kojim zahtjevom.
- **Vježba je samodostatna.** Podatak naveden u ranijoj vježbi ponavlja se.
- Na tehnikalijama se ne gubi vrijeme. Ako oznaka zapisa nije poznata unaprijed, u
  istom se retku kaže kojim je zahtjevom dobiti.
- Vježba ovisi o stanju koje prethodne vježbe ostavljaju. Provjeriti redoslijed.
- Zadatak „izbrišite redak i vidite da ne radi" je premekan: što god se izbriše, nešto
  prestane raditi. Vježba traži da se nađe točan redak i objasni zašto baš on.
- Vježba koja ne donosi ništa novo u odnosu na prethodni slajd ne postoji.

---

## 12. Pitanja

Retoričko pitanje ne ide na slajd. Slajd nosi tvrdnju.

Ondje gdje predavač želi pitati razred, slajd nosi prijelom (`\pause`), a odgovor
dolazi iza njega. Pitanje se ne ispisuje: student koji slajdove gleda kod kuće vidi
odgovor, a razred ga dobiva usmeno.

Pitanje smije stajati napisano na točno dva mjesta: kao zaključna rečenica vježbe i u
ponavljanju koje je izrijekom zamišljeno kao niz pitanja.

U ponavljanju odgovor nije ime funkcije iz projekta nego mjesto i razlog: „provjera
prije upisa, u sloju koji vidi i pošiljatelja i zapis". Cilj ponavljanja je temeljno
znanje, ne napamet naučena imena.

---

## 13. Postupak

### Redoslijed rada

1. Odrediti jedan do dva ishoda. Sve dalje postoji zato da do njih dovede.
2. Provjeriti stanje referentnog projekta na kraju toga tjedna, uz oznaku iz cjeline 19.
   Time se zna što student već ima pred sobom, a što tek dolazi.
3. Podijeliti gradivo na tri do pet cjelina i napisati rečenicu koja svaku opisuje. Ta
   rečenica je ujedno tekst razdjelnika. Cjelina kojoj se takva rečenica ne da napisati
   nije cjelina.
4. Napisati uvodni par problem-rješenje. On postavlja cijelo predavanje, pa se piše
   prvi, prije pojedinih slajdova.
5. Napisati slajdove cjelinu po cjelinu, s vježbom ondje gdje se gradivo može izvesti
   rukom.
6. Napisati sažetak iz onoga što na slajdovima stvarno stoji, ne iz plana.
7. Tri prolaza iz nastavka ove cjeline, pa prijevod i vizualna provjera iz cjeline 16,
   pa popis provjere na kraju.

### Dva do tri prolaza, uvijek

Predavanje se ne predaje iz prvog pisanja. Nakon što je tekst gotov:

1. **Prolaz za strukturu**: naslovi, redoslijed, nedostaje li slajd koji premošćuje
   dva pojma.
2. **Prolaz za registar**, rečenicu po rečenicu. Djelotvoran način: izvući samu prozu
   bez koda i tablica i pročitati je odvojeno, tražeći samo kalkove, razgovorne izraze
   i inverzivne pogodbene rečenice. Kao zaseban prolaz, ne usput.
3. **Prolaz za izgled**: tablice, prelamanje, visina okvira, prelijevanje.

Registar popušta u dugim sesijama. Nakon nekoliko sati rečenice počnu dobivati engleski
oblik, a provjera se svede na strukturu. Zato je drugi prolaz zaseban i radi se
svježim okom.

### Ispravak se primjenjuje u punom opsegu

Kad se jedna natuknica pokaže lošom, provjerava se cijeli dokument istim kriterijem.
Loše natuknice ne dolaze u parovima nego u jatima. Ispravak ide i u sažetak i u
razdjelnike cjelina.

### Popis provjere prije predaje

1. Prevodi se bez prelijevanja i bez pogrešaka, a stranica nije manje nego okvira.
2. Nijedan pojam nije upotrijebljen prije nego je uveden.
3. Nijedno drugo predavanje nije spomenuto, ni unaprijed ni unatrag.
4. Nijedna em-crtica.
5. Sve tvrdnje koje nisu propis stoje u okviru za konvenciju.
6. Nazivlje dosljedno, uključujući slike i dijagrame.
7. Tablice odvojene od naslova, ćelije u jednom retku gdje god je moguće.
8. Svaka putanja navedena u isječku postoji u repozitoriju.
9. Svaka apstraktna tvrdnja ima primjer.
10. Sažetak odražava stvarni sadržaj nakon svih izmjena.
11. Nijedno retoričko pitanje na slajdu.
12. Vježbe u istom obliku kao u ostalim predavanjima, bez navedenih ishoda.
13. Izmijenjene stranice pogledane kao slika, ne samo prevedene.

---

## 14. Obrazac slajdova

Uz ovaj dokument ide prevediv primjer: `Predavanja/obrazac/obrazac.tex` i njegov PDF.

Nije predavanje nego katalog oblika. Svaka cjelina imenuje jedan oblik slajda, njezin
razdjelnik kaže kada se taj oblik koristi, a slajd iza razdjelnika je primjer. U izvoru
iznad svakog okvira stoji komentar s imenom oblika i pravilom koje ga drži.

Obrađeni oblici: naslovnica, Plan predavanja, Ishodi učenja, Domena primjera, par
problem-rješenje s oznakama `(I)` i `(II)`, uvođenje pojma s primjerom izvan domene,
okvir za konvenciju, isječak s putanjom, dvije datoteke na istom slajdu, dijagram,
prijelom `\pause` za pitanje razredu, vježba i Sažetak.

Sadržaj primjera je uvjetni zahtjev i zaglavlje `ETag`. Ta tema namjerno nije ni u
jednom predavanju kolegija, pa se okviri smiju prepisivati kao oblik bez opasnosti da
se gradivo ponovi.

---

## 15. Preambula

Sva predavanja uključuju `Predavanja/common/preamble.tex`. Ondje su boje, fontovi,
zaglavlje, podnožje i logotipi, pa pojedino predavanje o izgledu ne odlučuje ništa.

Kostur novog predavanja:

```latex
% !TeX program = lualatex
% !TeX root = predavanjeNN.tex
\input{../common/preamble.tex}

\title[Predavanje N: Kratki naslov]{Programiranje za web \\ Predavanje N: Puni naslov}
\date{DD.MM.GGGG.}

\begin{document}
\frame{\titlepage}
...
\end{document}
```

Kratki naslov iz uglatih zagrada ide u podnožje, puni na naslovnicu. Puni naslov duži
od otprilike šezdeset znakova prelije naslovnu stranicu i zakloni podnaslov logotipa.
Prijevod to ne prijavi, vidi se samo na slici.

Što preambula nudi:

| Sredstvo | Oblik | Čemu služi |
|---|---|---|
| razdjelnik cjeline | `\sekcija{Naslov}{teme cjeline}` | otvara cjelinu i sam poziva `\section` |
| okvir za konvenciju | `\begin{konvencija}[Naslov] … \end{konvencija}` | tvrdnja koja nije propis |
| putanja datoteke | `\codefile{app/services/registration.py}` | putanje i nazivi slojeva |
| tipka ili naredba | `\kbd{Ctrl+C}` | ono što korisnik tipka |
| komentar u isječku | `<@\kom{tekst}@>` ispisuje `# tekst` | komentar uz redak koda |
| komentar u isječku TypeScripta, Vuea, CSS-a | `<@\komts{tekst}@>` ispisuje `// tekst` | isto, za jezike s `//` |
| stupac tablice | `L{3.2cm}` | stupac zadane širine, poravnat ulijevo |
| izlaz iz `listings` | `<@ … @>` | dijakritici i LaTeX unutar isječka |

Dvije napomene uz te makroe:

- `\kom{}` ispisuje ljestve, pa vrijedi samo za Python i bash. U TypeScriptu se
  komentar bez dijakritika piše doslovno, kao `//`, a komentar s dijakriticima kroz
  `\komts{}`, koji ispisuje `//` u istoj boji.
- Okolina `codeframe` postoji u preambuli, ali se ne koristi ni u jednom predavanju,
  jer nosi `shrink=5`. Za okvir s kodom ide obični `\begin{frame}[fragile]`.

---

## 16. Prijevod i provjera

Prijevod je `lualatex`, u dva prolaza, jer broj slajdova u podnožju dolazi iz prvog
prolaza. Na računalu na kojem su predavanja pisana MiKTeX nije na `PATH`, pa se zove
punom putanjom, `...\MiKTeX\miktex\bin\x64\lualatex.exe`.

```
cd Predavanja/predavanjeNN
lualatex -interaction=nonstopmode predavanjeNN.tex
lualatex -interaction=nonstopmode predavanjeNN.tex
```

Nakon drugog prolaza provjeriti troje u dnevniku i jedno u PDF-u:

| Provjera | Naredba | Cilj |
|---|---|---|
| pogreške | `grep -c '^!' predavanjeNN.log` | 0 |
| prelijevanja | `grep -c Overfull predavanjeNN.log` | 0 |
| broj stranica | `pdfinfo predavanjeNN.pdf` | ne manji od broja okvira |

Treća provjera hvata kvar koji prijevod ne prijavi. Pogreška u argumentu makroa za
razmak, recimo `\vspace{0.9horizontalem}`, pojede sadržaj okvira bez ijedne poruke, a
jedini je trag da je stranica manje nego okvira.

Izmijenjenu stranicu pogledati kao sliku, svaki put:

```
pdftoppm -f N -l N -r 100 -png predavanjeNN.pdf izlaz
```

To da se predavanje prevelo ne znači da izgleda dobro. Preklopljene oznake u dijagramu,
tablica koja dodiruje susjedni stupac i naslov koji je pao preko logotipa ne stvaraju
nijednu poruku u dnevniku.

---

## 17. Mjere

Kad dnevnik javi prelijevanje, kaže i za koliko. Iz toga se računa koliko sadržaja
treba van, umjesto da se pogađa:

- redak proze je oko `13.5 pt`
- redak u isječku koda je oko `8.5 pt`
- širina teksta je oko `12.8 cm`

Prelijevanje od `19 pt` je dakle jedan i pol redak proze, a od `9 pt` jedan redak
isječka. Prelijevanje manje od `3 pt` ne vidi se na slici, ali se svejedno ispravlja,
jer sljedeća izmjena na tom slajdu kreće iz minusa.

Redoslijed zahvata je uvijek isti: prijelom na dva slajda, pa brisanje cijele suvišne
tvrdnje, pa tek na kraju preoblikovanje rečenice. Smanjivanje fonta i razmaka nije
zahvat nego skrivanje problema.

---

## 18. Zamke u LaTeXu

- `listings` čita bajt po bajt, pa višebajtni znak premjesti: „početni" ispadne
  „čpoetni". `literate` to ne popravlja. Rješenje je izlaz u LaTeX: sve između `<@` i
  `@>` ne prolazi kroz `listings`. Unutar izlaza vrijede LaTeX pravila, pa se `_` piše
  `\_`. Izvan izlaza u isječku ostaje samo ASCII.
- Okvir koji sadrži `lstlisting` mora biti `[fragile]`.
- Podebljanje je `\textbf{}`. Markdown zvjezdice se ispisuju doslovno.
- `\uncover` u `p`-stupcu tablice traži `\leavevmode` ispred sebe, inače ćelija dobije
  prazan prvi redak i sadržaj padne jedan redak niže. Prijevod to ne prijavi.
- Uz `tabcolsep` postavljen na nulu ćelija koja točno ispuni svoju širinu dodiruje
  sljedeći stupac. I to se vidi tek na slici.
- Dvostruka obrnuta kosa crta u naredbenom retku ovisi o ljusci. Izmjene koje sadrže
  LaTeX naredbe pišu se u skriptu, ne u `python -c` ili `sed` iz ljuske, inače
  `\\vspace` završi kao `\v`, a `\t` kao tabulator.

---

## 19. Provjera uz repozitorij projekta

Predavanje tvrdi nešto o kodu, pa se prije predaje provjerava uz kod, ne po sjećanju.

Referentna aplikacija je zaseban repozitorij, `situnizd-pzw-projekt`. Stanje na kraju
tjedna N nosi oznaka `predavanje-NN`, pa se sadržaj datoteke iz tog tjedna čita
izravno:

```
git show predavanje-04:api/app/routers/lifters.py
```

Provjerava se ono što student može usporediti sa svojim zaslonom: putanje datoteka,
adrese ruta, statusni kodovi, oblik odgovora na pogrešku, nazivi polja, zadane
vrijednosti, nazivi testnih računa i način izolacije testova. Svaka od tih sitnica koja
se razilazi s kodom na vježbama vrijedi više izgubljenog povjerenja nego što je vrijedno
vrijeme ušteđeno na provjeri.

Dio kolegija za koji oznake ne postoje radi se drukčije. Ondje isječak ne nosi putanju,
osim kad je sama struktura mapa gradivo toga slajda, a tada se uvodi kao struktura koju
tek gradimo. Sve što se ipak može provjeriti provjerava se uz ugovor API-ja: adrese,
statusni kodovi, oblik pogreške, nazivi parametara za straničenje i vrijednosti koje
ruta prima. Taj ugovor stoji u `README.md` referentnog projekta i u `/docs` pokrenutog
poslužitelja.

---

## 20. Kako je gradivo raspoređeno

Raspored nije prijevod nekog izvora nego podjela na cjeline koje stanu u jedan termin i
nose jedan do dva ishoda. Kad se predavanje mijenja, provjerava se i granica prema
susjednima: gradivo koje je preraslo svoj termin seli, a ne zbija se.

| | Predavanje | Datum | Cjelina | Okvira | Stranica |
|---|---|---|---|---|---|
| p00 | O predmetu | 08.10.2026. | 2 | 9 | 12 |
| p01 | Arhitektura backenda i kostur projekta | 08.10.2026. | 5 | 32 | 38 |
| p02 | Modeliranje podataka, ORM i migracije | 15.10.2026. | 4 | 40 | 45 |
| p03 | Autentikacija i sigurnost | 22.10.2026. | 5 | 39 | 46 |
| p04 | Autorizacija i vlasništvo nad zapisom | 29.10.2026. | 6 | 47 | 57 |
| p05 | Oblikovanje API-ja i CRUD domene | 05.11.2026. | 4 | 59 | 65 |
| p06 | Poslovna pravila i rokovi | 12.11.2026. | 5 | 54 | 61 |
| p07 | Arhitektura jednostranične aplikacije | 26.11.2026. | 5 | 52 | 59 |
| p08 | Komunikacija s API-jem i prijava korisnika | 03.12.2026. | 5 | 57 | 64 |
| p09 | Upravljanje stanjem i stanja sučelja | 10.12.2026. | 4 | 53 | 60 |
| p10 | Tablice, filtri i radnje organizatora | 17.12.2026. | 4 | 50 | 56 |
| p11 | Testiranje cjelovite aplikacije | 07.01.2027. | 4 | 53 | 59 |
| p12 | Produkcijska izgradnja i postavljanje | 14.01.2027. | 3 | 52 | 57 |

Cjeline unutar svakog predavanja, onim redom kojim idu:

| | Cjeline |
|---|---|
| p01 | Od zahtjeva do odgovora; Ugovor prema klijentu; Kostur projekta; Dijagnostika i kvaliteta; Rad s verzijama koda |
| p02 | Baze podataka; Ograničenja i transakcije; Objektno-relacijsko preslikavanje; Migracije i početni podatci |
| p03 | Lozinke; Identitet u protokolu bez pamćenja; Implementacija autentikacije tokenom; Prijava i provjera zahtjeva; Što token ne rješava |
| p04 | Što autorizacija odlučuje; Provjera uloge; Slojevi aplikacije; Vlasništvo nad zapisom; Odgovori i njihove posljedice; Testiranje prava pristupa |
| p05 | Od zapisa do resursa; Svojstva HTTP metoda; Sheme; Popisi |
| p06 | Pravila koja shema ne može provjeriti; Stanje izvedeno iz vremena; Prijelaz stanja umjesto brisanja; Pogreška kao odgovor; Testiranje pravila koja ovise o vremenu |
| p07 | Stranica koja se ne učitava ponovno; Projekt u pregledniku; Prikaz koji prati podatke; Usmjeravanje u pregledniku; Izgled i sastavljanje aplikacije |
| p08 | Zahtjev iz preglednika; Jedno mjesto za slanje zahtjeva; Prijava i token; Token koji istekne; Zaštita prikaza i pogreške |
| p09 | Pohrana koju dijele prikazi; Stanja jednog prikaza; Obrasci i odbijeni zahtjevi; Ono što se ponavlja |
| p10 | Popis koji raste; Sužavanje popisa; Tablica i radnje nad retkom; Korisničko sučelje koje poznaje pravila |
| p11 | Što test dokazuje; Testovi poslužitelja; Testovi klijentskog dijela; Test kroz preglednik |
| p12 | Razvoj i produkcija; Postavljanje aplikacije; Što se mijenja kad aplikacija izađe van |

Granice koje se najlakše naruše, pa ih vrijedi držati na oku pri svakoj izmjeni:

- Provjera prava pristupa pripada predavanju o autorizaciji, a ne onome o oblikovanju
  API-ja, koliko god se u isječcima pojavljivala.
- Pravilo koje shema može provjeriti pripada predavanju o shemama; predavanju o
  poslovnim pravilima ostaje ono što traži bazu ili vrijeme.
- Tipiziranje podataka pripada onome predavanju u kojem se ti podatci prvi put pojave,
  ne jednom zajedničkom slajdu o tipovima.
- Testovi nisu cjelina jednog predavanja. Testiranje pravila koja se tada uvode ide uz
  ta pravila, a predavanju o testiranju ostaje ono što se ne može pokazati ranije:
  razine testova, pokrivenost, klijentski testovi i test kroz preglednik.
- Postavljanje u produkciju lako naraste u popis pojmova. Ostaje ono što se može
  izvesti i pokazati, a pojmovi koji se samo imenuju izlaze.

Mjera je uvijek ista. Student iz predavanja iznosi jedan do dva ishoda, a sve ostalo
na slajdu postoji zato da do njih dovede.
