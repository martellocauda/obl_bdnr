# obl_bdnr

## Búsqueda de código
ES en puerto por defecto 9200
Tener instalado python y pip3
pip3 install elasticsearch
pip3 install requests (no lo estamos usando ahora, pero instalar igual)
pip3 install flask
para correr: python code_search.py
levanta en http://localhost:5000/
La data de elasticsearch, por ahora insertarla manual

### crear index
curl -X PUT "localhost:9200/source_code_data?pretty"

### inserta data
curl -X POST "localhost:9200/source_code_data/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
    "owner" : "John Doe",
    "organization" : "AwesomeOrganization",
    "repository" : "AwesomeRepository",
    "visibility" : "Private",
    "codeLenguage" : "C#",
    "creationDate" : "2020-01-20",
    "licence" : "AwesomeLicenceType1",
    "fileName" : "AwesomeFile",
    "extension" : ".aw",
    "extra" : [ "AwesomeComment1", "AwesomeComment2" ],
    "sourceCode" : "function awesomeFunction (int: aw1, string: aw2) { echo awesome };",
    "codeViewLink" : "https://MyRepoUrl.com/repos/AwesomeRepository/"
}
'

curl -X POST "localhost:9200/source_code_data/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
    "owner" : "Franco Martello",
    "organization" : "TheBestOrganization",
    "repository" : "TeBestRepository",
    "visibility" : "Public",
    "codeLenguage" : "javascript",
    "creationDate" : "2020-06-13",
    "licence" : "TheBestLicenceType2",
    "fileName" : "ThisIsTheBestNew",
    "extension" : ".tb",
    "extra" : [ "BestComment1", "BestComment2" ],
    "sourceCode" : "function bestFunction (int: tb1, string: tb2) { echo thebesttt };",
    "codeViewLink" : "https://MyRepoUrl.com/repos/TheBestRepository/thebest.tb"
}
'

curl -X POST "localhost:9200/source_code_data/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
    "owner" : "Franco Martello",
    "organization" : "TheBestOrganization",
    "repository" : "TeBestRepository",
    "visibility" : "Public",
    "codeLenguage" : "javascript",
    "creationDate" : "2020-06-13",
    "licence" : "TheBestLicenceType2",
    "fileName" : "ThisIsTheBest",
    "extension" : ".tb",
    "extra" : [ "BestComment1", "BestComment2" ],
    "sourceCode" : "function bestFunction (int: tb1, string: tb2) { echo thebesttt };",
    "codeViewLink" : "https://MyRepoUrl.com/repos/TheBestRepository/thebest.tb"
}
'
