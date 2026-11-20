# Windows client screenshot sources

Captured on Windows on 2026-11-20 from EVP Remote 0.3.0, using the native Qt client UI at revision `55524bdd3f35060bac9309b647d432b58dc11f0d`. Each SVG contains one cropped PNG of the client area (without OS window decorations), numbered highlights, and a Chinese legend. No web reconstruction or generated UI is used.

| File | Captured state |
| --- | --- |
| `windows-settings.svg` | Connection settings, with an unsubmitted example server and an empty deployment key. |
| `windows-update.svg` | Settings → About shows the client version and the Check for updates button. No update request was sent or installation attempted. |
| `windows-host-share.svg` | Share this PC, before creating a temporary invitation. |
| `windows-join.svg` | Join form, before entering an invitation. |
| `windows-devices.svg` | A registered, online test client with an empty paired-device list. |
| `windows-pair.svg` | The requesting client with the other test client's pairing code entered and redacted. |
| `windows-pair-confirm.svg` | The receiving client with a real pending request, before manual approval. |
| `windows-trust-revocation.svg` | The newly paired, online peer selected; Remove pairing is available. |
| `windows-trust-removed.svg` | The same client after local removal. The list is empty and the status confirms that pairing is required again. |
| `windows-trusted-control.svg` | Trusted remote-control permission, shown unchecked. |
| `windows-session.svg` | A live direct session, video only: the host transmits synthetic color bars, a gray ramp, and a moving marker, not a desktop. |

The home and settings views use the shipping `HomeWindow` and `DesktopController` with temporary settings, separate test identity stores, and a loopback signaling server. Only private test windows received in-process events. Host labels, device IDs, and nonempty pairing codes were overwritten in raster pixels before export; the SVG does not retain an unredacted layer. The numbered highlights and legend are editorial annotations outside the client UI.

The session uses the project's unified host/viewer probe with a synthetic video source and recording input sink. For capture, the temporary probe read back the viewer's D3D11 back buffer before presentation and placed it at the native video child's measured bounds in the Qt window grab. The host generated the pattern before encoding; it was not drawn onto the screenshot. The loopback check reported a 640 × 360 source, 35 GPU-decoded and presented frames at sampling time, zero presentation failures, and no audio. No screen-wide capture, user desktop, real remote device, or OS-level input was used.
