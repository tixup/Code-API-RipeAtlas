L'obiettivo del test è valutare la capacità di un LLM di mantenere in memoria messaggi precedenti (fino a 2-3k token) 
e utilizzare una documentazione semplificata di RIPE Atlas (con esempi e dettagli) per generare codice in risposta a query specifiche. 
La documentazione di riferimento è contenuta all'interno di 'Ripe_Atlas_Basics.txt'.

Per ogni test, vengono forniti:
 - La query testuale inviata all'LLM.
 - Il codice generato in risposta.
 - L'output effettivo del codice eseguito.

Tra i numerosi esperimenti condotti, sono stati selezionati cinque test per ciascun modello, scelti in base a:
- Complessità della richiesta.
- Aderenza alle specifiche di RIPE Atlas.
- Tipologia di errori emersi durante l'esecuzione.

Ogni test è stato valutato secondo quattro criteri, ciascuno giudicato su una scala qualitativa a tre livelli, con una breve motivazione.

Si osserva che, generando nuove chat con gli stessi LLM, i risultati tendono a essere simili ma non identici, a causa del grado di libertà dell'LLM. 
Sono stati riportati i risultati "migliori" o quelli con gli errori più significativi e ricorrenti nei vari test eseguiti.
