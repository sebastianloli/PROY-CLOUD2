# Popeyes — Sistema de Gestión de Pedidos (CS2032)
## Kit de arranque · mantiene el Integrante 4

Este kit es la **base común** que clonan los 4 integrantes para que todo
encaje en una sola cuenta al final. La regla de oro: **todo es código**.
Nada se crea a mano en la consola; si no está en un `serverless.yml`,
no se podrá reproducir en la cuenta demo.

---

## 0. Lo que impone AWS Academy (leer primero)

- **Región única para los 4: `us-east-1`.**
- **No se puede crear nada en IAM** (ni usuarios ni roles). Existe un rol
  pre-creado llamado **`LabRole`** y es el que usamos para TODO.
- **Distinguir dos cosas que se confunden:**
  - *Quién despliega:* el **usuario temporal del lab** (las credenciales que
    copias de "AWS Details"). Caducan ~4 h y rotan cada sesión.
  - *Con qué se ejecutan las Lambdas / Step Functions:* el rol **`LabRole`**.
  - O sea: tú NO creas roles. Despliegas con el usuario del lab, y los
    recursos corren con `LabRole`.
- Cada quien trabaja en **su propia cuenta** durante el desarrollo. Al final
  se redespliega todo en **una sola cuenta demo** (la del Integrante 4).

### Refrescar credenciales cada sesión
1. En el lab: **Start Lab** → **AWS Details** → **AWS CLI**.
2. Copia el bloque (incluye `aws_access_key_id`, `aws_secret_access_key` y
   **`aws_session_token`**) a `~/.aws/credentials` bajo el perfil `default`.
3. Verifica: `aws sts get-caller-identity`

---

## 1. Instalar el framework serverless

Recomendado: **Serverless Framework v4** (es la versión vigente).

```bash
npm install -g serverless
serverless login   # cuenta gratuita, sin tarjeta. Una sola vez por máquina.
```

> v4 pide autenticarse una vez (es gratis por debajo de US$2M de ingresos,
> que es nuestro caso). El Access Key queda guardado en tu máquina.
>
> Alternativa sin login: `npm install -g serverless@3` (v3 sigue funcionando,
> pero ya no recibe mantenimiento). Si el equipo quiere cero cuentas externas,
> también vale **AWS SAM**. Cualquiera de las tres cumple el requisito de
> "framework serverless" del enunciado.

---

## 2. Convención de nombres (OBLIGATORIA)

Todo recurso lleva prefijo `pp-<servicio>-<recurso>`:

| Servicio        | Dueño        | Ejemplos                                  |
|-----------------|--------------|-------------------------------------------|
| `pp-platform`   | Integrante 4 | bus `pp-bus`, `pp-user-pool`              |
| `pp-orders`     | Integrante 1 | `pp-orders-table`, `pp-orders-api`        |
| `pp-kitchen`    | Integrante 2 | `pp-kitchen-sm`, `pp-tasks-table`         |
| `pp-integ`      | Integrante 3 | `pp-integ-rappi-fn`                       |

Esto evita choques cuando los 4 servicios convivan en la misma cuenta.

---

## 3. Orden de despliegue

`pp-platform` SIEMPRE va primero: crea el bus de eventos y el User Pool de
Cognito, y publica sus IDs en SSM Parameter Store. Los demás servicios los
leen con `${ssm:/pp/...}` (por eso nadie hardcodea ARNs).

```bash
# 1) Integrante 4 (en su cuenta y, al final, en la cuenta demo)
cd platform && serverless deploy

# 2) Cada microservicio (después de que platform exista en esa cuenta)
cd ../pp-orders && serverless deploy
```

Durante el desarrollo, cada integrante despliega `pp-platform` también en SU
cuenta, para tener bus + Cognito locales y poder probar con mocks.

---

## 4. Las 7 reglas para que al final NO cueste unir

1. Todo como código (IaC). Nada a mano en consola.
2. Rol dinámico: `arn:aws:iam::${aws:accountId}:role/LabRole` (el mismo código
   sirve en cualquier cuenta).
3. Cero ARNs hardcodeados → leer de SSM (`${ssm:/pp/...}`).
4. Contratos congelados el día 1 → ver `shared-config.json`.
5. Config compartida en Git, no en el chat.
6. OCI se conecta por **URL + API key** (no por IAM): al final solo se
   re-apunta la URL del API Gateway de la cuenta demo.
7. Ensayar el `deploy` completo en la cuenta demo 3–4 días antes del 05-jul.

---

## 5. Archivos de este kit

- `shared-config.json` — contratos (eventos, estados, nombres). Fuente única.
- `platform/serverless.yml` — bus `pp-bus` + Cognito + SSM (tu servicio).
- `_template-microservicio/` — plantilla que clonan Integrantes 1, 2 y 3.
