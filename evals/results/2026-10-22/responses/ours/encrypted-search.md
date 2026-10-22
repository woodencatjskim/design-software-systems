Exercise: encrypted-search

The requirements conflict: a server that cannot read message plaintext cannot also run ordinary workers that extract mentions, index plaintext, and generate previews from every message. Keep end-to-end encryption and move plaintext-dependent processing to authorized clients, or explicitly weaken the privacy contract. Do not present server decryption as end-to-end encryption.

With encryption preserved, use an established, audited messaging protocol and implementation supporting groups and multiple devices. Servers authenticate users, enforce conversation membership, store ciphertext, and route opaque envelopes. They may still observe transport metadata such as recipients, timing, and sizes; minimize retention according to the product's privacy requirements.

Clients parse mentions before encryption and render them after decryption. Push notifications can be generic. If the server must route special mention notifications, clients can send explicit recipient hints, but that exposes mention metadata and needs user-visible privacy acceptance. A server cannot verify those hints against unreadable plaintext.

Each device builds a local full-text index from decrypted history. Server workers cannot build the requested plaintext index. Searching on a second device requires that device to obtain authorized history and build its own index, or an explicitly designed encrypted index-transfer feature. Specialized searchable encryption is not an automatic replacement for ordinary full-text search and would require a separate security evaluation.

For link previews, a sending client can fetch a preview and include its title/image inside the encrypted message. Fetching directly exposes a visit to the destination; remote fetching exposes the URL to the preview service. Offer a preview consent/disable policy and validate remote content. Generating previews on every message at a server requires disclosing links or plaintext, so that requirement must change.

For media, encrypt attachments on the client with protocol-supported mechanisms. Upload ciphertext to private object storage; send its locator, integrity information, and decryption material inside the encrypted conversation. Authorize object access separately. Servers cannot perform ordinary plaintext malware scanning or media transformations without changing the trust model; client-side validation and supported client transformations replace those capabilities.

A second device is a new cryptographic endpoint, not merely another login session. Use the selected protocol's authenticated device enrollment and key distribution, with existing-device approval or an established recovery method. Deliver future messages to authorized device identities. Share old history through secure device-to-device transfer or an explicitly protected encrypted backup; do not assume future message keys unlock all history. Revoke devices through the protocol's membership/key-update process. Revocation cannot erase plaintext already copied to a device.

Validate enrollment, revocation, backup recovery, multi-device fanout, and missing-history behavior against the chosen library. No new cryptographic protocol is proposed here.
