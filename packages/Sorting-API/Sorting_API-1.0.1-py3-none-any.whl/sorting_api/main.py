
from fastapi import FastAPI
from sorting_api.routing.router import router

app = FastAPI(
    title="Sorting API",
    description=(
        "L'API offre due semplici funzionalità: \n"
        "- Effettua l'ordinamento, crescente o decrescente, di un array attraverso "
        "un algoritmo di sorting tra quelli disponibili: " +
        " Bubblesort, Insertionsort, Selectionsort, Mergesort \n"
        "- Disordina un array, ridisponendo i suoi elementi in modo casuale \n\n" +
        "Gli auturi sono: \n" + 
        "- Andrea Broccoletti [886155] \n" +
        "- Simone Lesinigo [899540]"
    ),
    version="1.0.0",
)
app.include_router(router)