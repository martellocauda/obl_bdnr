# obl_bdnr

## Búsqueda de código
ES en puerto por defecto 9200 <br />
Tener instalado python y pip3 <br />
pip3 install elasticsearch <br />
pip3 install requests (no lo estamos usando ahora, pero instalar igual) <br />
pip3 install flask <br />
source code_search/bin/activate <br />
para correr: python code_search.py <br />
levanta en http://localhost:5000/ <br />
La data de elasticsearch, por ahora insertarla manual <br />

### crear index
curl -X PUT "localhost:9200/source_code_data?pretty" <br />

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
