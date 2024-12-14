# 2024_assignment2_Mongo-DevOps
## **Gruppo ErbaFiore**
**Autori:**
- Erba Lorenzo 933012
- Fiorentini Nicolò 933157

## Link repository

https://gitlab.com/me8845048/2024_assignment_mongo-devops

## **Introduzione**

Il repository *2024_assignment2_Mongo-DevOps* è stato realizzato per fornire un'implementazione di una pipeline CI/CD, tramite GitLab, per la parte di sviluppo DevOps di un'applicativo software.


## **Scopo del progetto**

Lo scopo del progetto è quello di realizzare una pipeline CI/CD, tramite infrastruttura GitLab, la quale garantisca che ogni modifica apportata al codice sorgente, prima di essere pubblicata e resa disponibile (deploy del software), venga sottoposta a un processo di controllo e di verifica di alcuni requisiti. Questo permette di migliorare la qualità del software, andando a ridurre gli errori e la probabilità di rilascio di un software insicuro e/o poco efficiente, in modo del tutto automatizzato. 


## **Contenuto del repository**

Il repository è organizzato nel seguente modo:

```bash
│   .gitlab-ci.yml
│   .pylintrc
│   mkdocs.yml
│   README.md
│   requirements.txt
│   setup.py
│
├───App
│       .gitkeep
│       main.py
│       MyDbConnection.py
│
├───docs
│       index.md
│
└───tests
    ├───integration
    │   │   .gitkeep
    │   │   integration-test.py
    │
    ├───performance
    │   │   .gitkeep
    │   │   performance-test.py
    │   
    │
    └───unit
        │   .gitkeep
        │   unit-test.py
```

## **Realizzazione del progetto**

La pipeline fa riferimento al software presente nella cartella *App*, ovvero un progetto in Python che gestisce una connessione a un database MongoDB, al quale viene effettuata una semplice interrogazione di ricerca all'interno della collezione. 

La cartella *App* contiene i seguenti file:

- main.py: corrisponde allo script eseguibile dell'applicazione.
- MyDbConnection.py: corrisponde a uno script per effettuare connessione, disconnesione e query al database remoto.

All'interno della cartella *tests* sono presenti:

- unit-test.py, che esegue test di unità sul modulo *MyDbConnection.py*.
- performance-test.py, che valuta il tempo d'esecuzione necessario per la connessione e per ottenere una risposta dal database. 
- integration-test.py, che valuta l'interazione e integrazione fra i vari moduli.

All'interno della root del repository troviamo i seguenti file:

- *.gitlab-ci.yml*: uno script scritto in linguaggio YAML per la realizzazione della pipeline CI/CD.
- *.pylintrc*: file di configurazione per pylint.
- *setup.py*: script utilizzato per configurare e distribuire pacchetti Python.
- *mkdcos.yml*: file di configurazione per il modulo *mkdocs* per la generazione della documentazione.
- *requirements.txt*: file testuale contenente i moduli da installare per poter eseguire il codice sorgente correttamente.

## **Stato attuale del progetto**

Il progetto richiede l'implementazione dei seguenti stage all'interno della pipeline: 

- [X] Build
- [X] Verify
- [X] Test
- [X] Package
- [X] Release
- [X] Docs.

Lo stage Verify risulta, attualmente, parzialmente completo, in quanto nel primo stage non è stata implementata un'analisi dinamica del codice. Si è pensato di implementare un profiling della memoria tramite memory_profiler.

## Documentazione
Per la realizzazione dell'ultimo stage, Docs, è stata realizzata una [documentazione](docs/index.md) riassuntiva di ogni stage implementato nella pipeline, presente all'interno della cartella docs. Tale documentazione inoltre è stata pubblicata come pagina web all'interno di GitLab Pages.

## Scelte e motivazioni
Durante lo sviluppo di questo progetto sono state effettuate alcune scelte, tra cui:

- utilizzo di variabili d'ambiente in GitLab per mascherare password e token. In questo modo si garantisce maggiore sicurezza e protezione nei confronti di accessi al database e pubblicazioni di pacchetti non autorizzati.

- bypass dell'esecuzione della pipeline qual'ora venissero modificati file come ```README.md``` oppure ```docs/index.md```. L'implementazione dello skip d'esecuzione permette di eseguire la pipeline solo quando avvengono modifiche su file che riguardano direttamente l'esecuzione della pipeline di automazione.

- utilizzo di un file ```.pylintrc```. L'utilizzo di questo file permette di evitare, nello stage di ```verifiy``` l'analisi statica del file ```MyDbConnection.Py``` in quanto lo scopo di questo progetto è dimostrare padronanza nell'utilizzo della pipeline di automazione e non di effettuare linting del codice.

- sviluppo di test elementari. Analogamente con quanto detto nel punto precedente, la suite di test sviluppata per questo progetto contiene test elementari, dove l'unico obbiettivo è poter eseguire vari test nella pipeline di automazione.

