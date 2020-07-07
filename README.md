# obl_bdnr

## Verificaciones previas
Tener ES en puerto por defecto 9200 y localhost <br />
Tener REDIS en puerto por defecto 6379 y localhost <br />
Tener instalado python3.6 y pip3 <br />

## Pasos
Crear un nuevo virtualenv: python3 -m venv github <br />
Imaginemos que la ruta del nuevo venv se crea en /srv/github/ <br />
Clonar repo <br />
Imaginemos que la ruta del repo es /srv/obl_bdnr/ <br />
Activar venv: source /srv/github/bin/activate <br />
Chequear bin de python: which python <br />
Instalar requerimientos: pip3 install -r /srv/obl_bdnr/requirements.txt <br />
Para correr: python /srv/obl_bdnr/github.py <br />
La app levanta en http://localhost:5000/ <br />
La data de elasticsearch, insertarla manual (curl por curl). Está en el archivo /srv/obl_bdnr/inserts_elasticsearch.txt <br />
