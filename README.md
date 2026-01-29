# Python DNS Proxy Server

<!--toc:start-->
- [Python DNS Proxy Server](#python-dns-proxy-server)
  - [Modo de uso](#modo-de-uso)
  - [Parámetros](#parámetros)
  - [Ejemplo de archivo de configuración](#ejemplo-de-archivo-de-configuración)
    - [Ejemplo de funcionamiento (tomando en cuenta la configuración anterior)](#ejemplo-de-funcionamiento-tomando-en-cuenta-la-configuración-anterior)
<!--toc:end-->

## Modo de uso

El script tomará los argumentos que el usuario le pase por consola si es que no existe un archivo de configuración en la ruta `$HOME/.config/dns-proxy/settings.toml`. Para cada argumento que el usuario no ingrese, se tomará su valor por defecto. Si el archivo de configuración existe, se tomarán los valores del mismo ignorando así los argumentos pasados por la línea de comandos, a menos que se especifique la flag `--force-args`, la cual forzará al script a usar los argumentos pasados por consola por encima de los del archivo de configuración, pero aún así, los valores del archivo de configuración reemplazarán a los valores por defecto para cada campo. El archivo de configuración se puede crear al introducir el parámetro `--save-config`, en el cual se guardarán todos los valores pasados como argumento.

La sección `map` del archivo de configuración será utilizada para asignarle una IP a un dominio de forma manual. Cada vez que se pregunte por ese dominio, se responderá con la IP que se le asigne.

La sección `exceptions` del archivo de configuración será utilizada para verificar si la IP desde donde se hace la petición coincide con alguna de las IPs a las que está mapeado el dominio por el que se pregunta. Si es así, se forzará al servidor DNS proxy local a hacerle una petición al servidor DNS remoto por ese dominio, incluso si ese dominio está manualmente mapeado una dirección IP en la sección `map`. Si otro IP pregunta por ese dominio, se le responderá de acuerdo al contenido de la sección `map`.

La sección `vars` será utilizada para declarar lo que serán variables. Por ejemplo, si se introduce `ip = "8.8.8.8"`, se podrá acceder a esa IP desde cualquiera de las secciones `map` o `exceptions` simplemente referenciando a esa variable con el formato `${VARIABLE}`, en este caso, `${ip}`. Si en la sección `map` hay una asignación de la siguiente forma: `"domain.com" = "${ip}"`, al dominio `domain.com` le será asignado como IP el valor de la variable `ip`.

## Parámetros

- port : Puerto local por el cual el servidor estará a la escucha. Por defecto 53.

- -b, --bind \<address> : Interfaz por la cual actuará el servidor. Por defecto todas las interfaces (0.0.0.0).

- -u, --upstream \<address>:\<port> : Servidor DNS de destino. Por defecto 1.1.1.1 por el puerto 53 (1.1.1.1:53).

- -t, --timeout : Tiempo máximo a esperar por la respuesta del servidor de destino. Por defecto 5 segundos. Si pasa ese tiempo, el servidor proxy enviará la respuesta NXDOMAIN (Non-Existent Domain).

- --log-format \<log_format> : Formato de salida de los logs.

- --log-prefix : Si incluir en los logs la hora del evento y otros metadatos.

- --save-config \[path] : Archivo en el cual guardar los valores de los argumentos pasados al script (excepto --save-config y --force-args). Se comportará de la siguiente manera:
  1. No se especifica la flag ni su argumento: No se guardará la configuración en un archivo.
  2. Se especifica la flag pero no su argumento: Se guardará la configuración en un archivo en la ruta por defecto `$HOME/.config/dns-proxy/settings.toml`.
  3. Se especifica la flag con su argumento: Se usará ese nombre de archivo como el nombre del archivo de configuración.

- --force-args : Actúa como flag. Si se especifica, se usarán los argumentos introducidos por consola y se ignorarán los valores contenidos en el archivo de configuración. Por defecto se utiliza el archivo de configuración al leer los valores.

TODO: change format of specified values for --map and --exceptions

- -m, --map \<dominio:ip> : Si se especifica, debe pasarse como argumento almenos un par \<dominio:ip>. Si se pasarán mas de un par, deben ir separados o por comas, o introducir varios argumentos -m.

- -x, --exceptions \<dominio:ip> : Si se especifica, debe pasarse como argumento almenos un par \<dominio:ip>. Si se pasarán mas de un par, se deben introducir varios argumentos -x.

- --logs-file \<path> : Archivo en el cual guardar los logs del servidor. Si no se especifica, el archivo por defecto se encontrará en `$HOME/.config/dns-proxy/dns.log`.

## Ejemplo de archivo de configuración

```toml
[settings]
laddress = "192.168.1.2"
lport = 53
uaddress = "8.8.4.4"
uport = 53
timeout = 5
log_format = "request,reply,truncated,error"
log_prefix = true
logs_file = "path/to/logs/file.log"

[vars]
ip = "192.168.1.10"

[map]
"personal.domain1" = "${ip}"
"personal.domain2" = "192.168.42.86"
"www.personal.domain3" = "192.168.1.1"

[exceptions]
"www.personal.domain3" = "192.168.42.86"
```

### Ejemplo de funcionamiento (tomando en cuenta la configuración anterior)

```
IP <192.168.1.10> pregunta por el dominio <personal.domain1>
DNSProxy responde a <192.168.1.10>: <personal.domain1> está en <192.168.1.10>

IP <192.168.1.12> pregunta por el dominio <personal.domain5>
DNSProxy pregunta a servidor remoto <8.8.4.4> por el dominio <personal.domain5>
DNSProxy responde a <192.168.1.12> con la respuesta del servidor remoto <8.8.4.4>

IP <192.168.42.85> pregunta por el dominio <www.personal.domain3>
DNSProxy responde a <192.168.42.85>: <www.personal.domain3> está en <192.168.1.1>

IP <192.168.42.86> pregunta por el dominio <www.personal.domain3>
DNSProxy pregunta a servidor remoto <8.8.4.4> por el dominio <www.personal.domain3>
DNSProxy responde a <192.168.42.86> con la respuesta del servidor remoto <8.8.4.4>
```
