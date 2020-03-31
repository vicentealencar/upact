ulysses start
  - Updates firewall rules. This command will 

ulysses stop
  - Stops the firewall. Requires superuser privileges

ulysses blocked_nameservers --enable --url="file where the blocked nameserver ips are located"
  - Enables blocking nameservers from being used. This might be useful for enforcing the usage of safe browsing DNSes (like CleanBrowsing)

ulysses blocked_nameservers --update
  - Updates the list of blocked DNSes. Requires admin privileges

ulysses blocked_nameservers --disable
  - Disables blocking nameservers. Requires admin privileges

ulysses block-sites --add="www.google.com,google.com" --playtime_days="every week" --playtime_hours="13:00-15:00" --playtime_hours="18:00-19:00"

ulysses block-sites --remove="www.google.com"
  - Requires admin privileges if rules have already been persisted

ulysses block-sites --persist
  - Marks the new rules for being persisted
