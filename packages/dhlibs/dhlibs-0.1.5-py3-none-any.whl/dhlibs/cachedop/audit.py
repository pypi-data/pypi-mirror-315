# This file is part of dhlibs (https://github.com/DinhHuy2010/dhlibs)
#
# MIT License
#
# Copyright (c) 2024 DinhHuy2010 (https://github.com/DinhHuy2010)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

from typing_extensions import Any, Mapping

from dhlibs.alias_callable import alias_callable
from dhlibs.cachedop._typings import AuditCallableType, AuditDefaultDict, AuditEvent, AuditEvents


def _resolve_events(events: AuditEvents) -> list[AuditEvent]:
    out: list[AuditEvent] = []
    if events is None:
        out.extend(getattr(AuditEvent, name) for name in AuditEvent._member_names_)
    elif isinstance(events, AuditEvent):
        out.append(events)
    else:
        out.extend(events)
    return out


class Auditer:
    def __init__(self) -> None:
        self._events = AuditDefaultDict(list)

    def register(self, callback: AuditCallableType, on_events: AuditEvents = None) -> None:
        for event in _resolve_events(on_events):
            self._events[event].append(callback)

    def clear(self, events: AuditEvents) -> None:
        for event in _resolve_events(events):
            self._events[event].clear()

    def audit(self, event: AuditEvent, args: Mapping[str, Any]):
        args = dict(args)
        for callback in self._events[event]:
            callback(event, args)


audit = Auditer()
register_audit_callback = alias_callable(audit.register, "register_audit_callback", qualname="register_audit_callback")
