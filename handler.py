import json
import os

# Stubs minimos para que 'serverless deploy' funcione de una.
# Cada integrante reemplaza la logica por la suya.

EVENT_BUS = os.environ.get("EVENT_BUS", "pp-bus")
TABLE = os.environ.get("TABLE", "pp-CHANGEME-table")


def crear(event, context):
    # El tenant viaja en el JWT validado por el authorizer de Cognito.
    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )
    tenant_id = claims.get("custom:tenant_id", "desconocido")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"ok": True, "tenantId": tenant_id, "msg": "stub creado"}),
    }


def on_evento(event, context):
    # Evento entrante desde pp-bus (ej. order.created)
    print("evento recibido:", json.dumps(event))
    return {"ok": True}
