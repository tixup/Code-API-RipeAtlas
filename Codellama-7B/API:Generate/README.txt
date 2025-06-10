Sono state eseguite diverse query in linguaggio naturale su modelli LLM, variando precisione e complessità per valutarne l'interazione con le API di RIPE Atlas 
senza alcun contesto aggiuntivo. 
Le richieste, inviate tramite chiamate REST all'endpoint /api/generate, sono state elaborate in sessioni indipendenti, senza memoria tra una query e l’altra. 
I modelli hanno dimostrato di non possedere una conoscenza aggiornata o sufficiente delle API RIPE Atlas, limitando la loro capacità di generare codice corretto senza supporto esterno.

Le query, formulate in inglese per coerenza con l'addestramento, hanno prodotto risultati variabili anche a parità di input, riflettendo la natura probabilistica degli LLM. 
Durante i test, sono emersi casi con output parzialmente corretti, errori critici o comportamenti inattesi. 
Per una presentazione chiara, sono stati selezionati tre test complessivi, per ciascun modello, privilegiando quelli più rappresentativi delle sfide nell'uso di API complesse come RIPE Atlas.
