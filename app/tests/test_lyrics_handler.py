import pytest
from unittest.mock import patch
from app.handlers.lyrics_handler import create_lyrics_set_list, trim_lyrics, get_translated_lyrics

def test_trim_lyrics():
    lyrics = "\nHello\nWorld\n"
    trimmed_lyrics = trim_lyrics(lyrics)
    print(trimmed_lyrics)
    assert trimmed_lyrics == "Hello\nWorld"  # Should remove the empty lines before and after

def test_create_lyrics_set_list():
    lyrics = "Hello\nHello\nWorld\n"
    lyrics_set_list = create_lyrics_set_list(lyrics)
    assert len(lyrics_set_list) == 2  # Duplicates should be removed
    assert "Hello" in lyrics_set_list
    assert "World" in lyrics_set_list



# Example lyrics for "NI BIEN NI MAL"
lyrics = """
[Intro: Bad Bunny]
Yeh-yeh
Yeh-yeh
Yeh-yeh

[Coro: Bad Bunny]
Sin ti no me va bien, tampoco me va mal (Yeah)
Pase lo que pase no te voy a llamar
Ya yo me quit√©, t√∫ nunca me va' a amar (Na)
Pa' no pensar en ti tengo que fumar
Sin ti no me va bien, tampoco me va mal
Pase lo que pase no te voy a llamar
Ya yo me quit√©, t√∫ nunca me va' a amar
Pa' no pensar en ti, tengo que fumar

[Verso 1: Bad Bunny]
Hoy voy a romper la noche, hoy yo voy a janguear (Wuh-huh)
Hoy voy a prender y no lo voy a pasar (Yeh)
Te juro por mami que en ti no vo'a pensar
Errores como t√∫ no me vuelven a pasar (Yeh)
A veces las noches se vuelven martirio
Como nuestro amor que se volvi√≥ un delirio
Mi alma est√° en guerra, es terreno sirio (Ey)
Las botellas de vino terminan en vidrios (Ey)
Y tu puteando, en verdad que te envidio (Ey)
Pero nada
T√∫ vas a extra√±arme cuando abras la cartera y no tengas nada
Cuando √©l te lo meta y no sientas nada
Cuando te sientas sola, perdida en la nada
T√∫ puedes arreglarlo, pero no haces nada
Baby, gracias por nada (Ey)
Ahora sobran los totos y los chavos (Ey)
Tu amiga dando like, si le meto, la grabo (Ey)
Me cago en tu madre y la de tu abogado
Prende la radio, te dejo un recado

[Coro: Bad Bunny]
Sin ti no me va bien, tampoco me va mal (¬°Yeh!)
Pase lo que pase no te voy a llamar (¬°No!)
Ya yo me quit√©, t√∫ nunca me va' a amar
Pa' no pensar en ti, tengo que fumar (Prr-prr-prrr)
Sin ti no me va bien, tampoco me va mal
Pase lo que pase no te voy a llamar
Ya yo me quit√©, t√∫ nunca me va' a amar
Pa' no pensar en ti tengo que fumar, ah, ah

[Verso 2: Bad Bunny & Miky Woodz]
Lo mejor de todo es que ahora pa' salir
No tengo que esperar que te termines de vestir
Hoy es noche 'e maldad y me voy a divertir
A tu amiga la acabo 'e partir
Como dice Miky: "No te vo' a mentir" (No te vo' a mentir; Prr-prr-prr)
Fui uno m√°s de tu colecci√≥n
No s√©, entre t√∫ y yo ya no hay conexi√≥n
Pa'l carajo el perd√≥n, no hay reconciliaci√≥n
Ahora te toca llorar en tu habitaci√≥n
(Porque ni por Dios cojo una llamada tuya)
Yo nunca forzo, dejo que todo fluya
(Te pasas en las redes tir√°ndome puya')
Quieren mi vida y no pueden con la suya

[Coro: Bad Bunny]
Sin ti no me va bien, tampoco me va mal
Pase lo que pase no te voy a llamar
Ya yo me quit√©, t√∫ nunca me va' a amar
Pa' no pensar en ti, tengo que fumar

[Outro: Bad Bunny]
Sin ti no me va bien, tampoco me va mal
Pase lo que pase no te voy a llamar
Ya yo me quit√©, t√∫ nunca me va' a amar
Pa' no pensar en ti, tengo que fumar
"""