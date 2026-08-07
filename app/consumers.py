"""Kafka consumers for reminders-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("reminders-service.consumers")

TABLE = "reminders"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("appointment.booked")
    def _on_appointment_booked(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    db.execute(f"INSERT INTO {TABLE} (data) VALUES (%s)",
                               (Json({"appointment_id": data.get("id"),
                                      "patient_id":     data.get("patient_id"),
                                      "send_at": data.get("start_time"),
                                      "status": "scheduled"}),))
        except Exception as e:
            log.exception("reminders-service/appointment.booked handler failed: %s", e)
        emit_audit(bus, action="consume.appointment.booked", actor="system:reminders-service",
                   target=None, details={"envelope_id": envelope.get("id")})

