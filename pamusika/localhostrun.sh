(base) macbook@MacBooks-MacBook-Air WA_Cloud % brew install ngrok

==> Auto-updating Homebrew...
Adjust how often this is run with HOMEBREW_AUTO_UPDATE_SECS or disable with
HOMEBREW_NO_AUTO_UPDATE. Hide these hints with HOMEBREW_NO_ENV_HINTS (see `man brew`).
==> Auto-updated Homebrew!
Updated 2 taps (homebrew/core and homebrew/cask).
==> New Formulae
asm6809                flexiblas              graphviz2drawio        mariadb@11.4           pgcopydb               xroar
boost@1.85             gabo                   http-server-rs         nuspell                tevent
dependabot             gfxutil                kea                    packcc                 tmpmail
dwarfs                 go@1.22                kubernetes-cli@1.30    passt                  truetree
fast_float             gql                    ldb                    pcaudiolib             ufbt
==> New Casks
approf                      kindle-create               labplot                     localcan                    nrf-connect

You have 11 outdated formulae installed.

==> Caveats
To install shell completions, add this to your profile:
  if command -v ngrok &>/dev/null; then
    eval "$(ngrok completion)"
  fi

==> Downloading https://raw.githubusercontent.com/Homebrew/homebrew-cask/f3046f799c32d169398e9940d00018c3535ec8f6/Casks/n/ngrok.rb
##################################################################################################################################### 100.0%
==> Downloading https://bin.equinox.io/a/2AVq3uXxS2b/ngrok-v3-3.14.1-stable-darwin-amd64.zip
##################################################################################################################################### 100.0%
==> Installing Cask ngrok
==> Linking Binary 'ngrok' to '/usr/local/bin/ngrok'
🍺  ngrok was successfully installed!
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ngrok http 5000

http - start an HTTP tunnel

USAGE:
  ngrok http [address:port | port] [flags]

AUTHOR:
  ngrok - <support@ngrok.com>

COMMANDS: 
  config          update or migrate ngrok's configuration file
  http            start an HTTP tunnel
  tcp             start a TCP tunnel
  tunnel          start a tunnel for use with a tunnel-group backend

EXAMPLES: 
  ngrok http 80                                                 # secure public URL for port 80 web server
  ngrok http --domain baz.ngrok.dev 8080                        # port 8080 available at baz.ngrok.dev
  ngrok tcp 22                                                  # tunnel arbitrary TCP traffic to port 22
  ngrok http 80 --oauth=google --oauth-allow-email=foo@foo.com  # secure your app with oauth

Paid Features: 
  ngrok http 80 --domain mydomain.com                           # run ngrok with your own custom domain
  ngrok http 80 --allow-cidr 2600:8c00::a03c:91ee:fe69:9695/32  # run ngrok with IP policy restrictions
  Upgrade your account at https://dashboard.ngrok.com/billing/subscription to access paid features

Upgrade your account at https://dashboard.ngrok.com/billing/subscription to access paid features

Flags:
  -h, --help      help for ngrok

Use "ngrok [command] --help" for more information about a command.

ERROR:  authentication failed: Usage of ngrok requires a verified account and authtoken.
ERROR:  
ERROR:  Sign up for an account: https://dashboard.ngrok.com/signup
ERROR:  Install your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken
ERROR:  
ERROR:  ERR_NGROK_4018
ERROR:  https://ngrok.com/docs/errors/err_ngrok_4018
ERROR:  
(base) macbook@MacBooks-MacBook-Air WA_Cloud % npm install -g localtunnel

npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules/localtunnel
npm ERR! errno -13
npm ERR! Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules/localtunnel'
npm ERR!  [Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules/localtunnel'] {
npm ERR!   errno: -13,
npm ERR!   code: 'EACCES',
npm ERR!   syscall: 'mkdir',
npm ERR!   path: '/usr/local/lib/node_modules/localtunnel'
npm ERR! }
npm ERR! 
npm ERR! The operation was rejected by your operating system.
npm ERR! It is likely you do not have the permissions to access this file as the current user
npm ERR! 
npm ERR! If you believe this might be a permissions issue, please double-check the
npm ERR! permissions of the file and its containing directories, or try running
npm ERR! the command again as root/Administrator.

npm ERR! A complete log of this run can be found in: /Users/macbook/.npm/_logs/2024-08-25T11_35_10_960Z-debug-0.log
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh -R 80:localhost:8080 ssh.localhost.run
The authenticity of host 'ssh.localhost.run (3.234.18.192)' can't be established.
RSA key fingerprint is SHA256:FV8IMJ4IYjYUTnd6on7PqbRjaZf4c1EhhEBgeUdE94I.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? no 
Host key verification failed.
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh -R 80:localhost:5000 ssh.localhost.run

The authenticity of host 'ssh.localhost.run (54.172.225.3)' can't be established.
RSA key fingerprint is SHA256:FV8IMJ4IYjYUTnd6on7PqbRjaZf4c1EhhEBgeUdE94I.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'ssh.localhost.run' (RSA) to the list of known hosts.

===============================================================================
Welcome to localhost.run!

Follow your favourite reverse tunnel at [https://twitter.com/localhost_run].

To set up and manage custom domains go to https://admin.localhost.run/

More details on custom domains (and how to enable subdomains of your custom
domain) at https://localhost.run/docs/custom-domains

If you get a permission denied error check the faq for how to connect with a key or
create a free tunnel without a key at [http://localhost:3000/docs/faq#generating-an-ssh-key].

To explore using localhost.run visit the documentation site:
https://localhost.run/docs/

===============================================================================

** your connection id is 47d37c73-f66c-42d5-8056-08215de6fda1, please mention it if you send me a message about an issue. **

macbook@ssh.localhost.run: Permission denied (publickey).
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh -o PubkeyAuthentication=no -R 80:localhost:5000 ssh.localhost.run


===============================================================================
Welcome to localhost.run!

Follow your favourite reverse tunnel at [https://twitter.com/localhost_run].

To set up and manage custom domains go to https://admin.localhost.run/

More details on custom domains (and how to enable subdomains of your custom
domain) at https://localhost.run/docs/custom-domains

If you get a permission denied error check the faq for how to connect with a key or
create a free tunnel without a key at [http://localhost:3000/docs/faq#generating-an-ssh-key].

To explore using localhost.run visit the documentation site:
https://localhost.run/docs/

===============================================================================

** your connection id is ba1b421d-acd2-4716-b20d-431428d08ec1, please mention it if you send me a message about an issue. **

macbook@ssh.localhost.run: Permission denied (publickey).
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-keygen -t rsa -b 4096 -C "nyakudyamufa2002@gmail.com"

Generating public/private rsa key pair.
Enter file in which to save the key (/Users/macbook/.ssh/id_rsa): mufaro
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in mufaro
Your public key has been saved in mufaro.pub
The key fingerprint is:
SHA256:iDP9vhhRVHeJ0azwa5LnsAJG3Amm48pehhSNFu6dXXU nyakudyamufa2002@gmail.com
The key's randomart image is:
+---[RSA 4096]----+
|  .     ..o E=.. |
| . +  o. ..o..+  |
|  = .+ oo. o .   |
| o oo=o+o   o    |
|  o.*o= S  . .   |
| . ..ooo  + +    |
| ...o....  B     |
|  oo   +. . .    |
| ..   . oo       |
+----[SHA256]-----+
(base) macbook@MacBooks-MacBook-Air WA_Cloud % eval "$(ssh-agent -s)"

Agent pid 86373
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~/.ssh/id_rsa

/Users/macbook/.ssh/id_rsa: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~/.ssh/id_rsa/mufaro

/Users/macbook/.ssh/id_rsa/mufaro: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % /Users/macbook/.ssh/id_rsa
zsh: no such file or directory: /Users/macbook/.ssh/id_rsa
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~/Users/macbook/.ssh/id_rsa 
/Users/macbook/Users/macbook/.ssh/id_rsa: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~/mufaro

/Users/macbook/mufaro: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~//Users/macbook/.ssh/id_rsa/mufaro
/Users/macbook//Users/macbook/.ssh/id_rsa/mufaro: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % find ~ -name "mufaro*"

find: /Users/macbook/Pictures/Photos Library.photoslibrary: Operation not permitted
/Users/macbook/Desktop/my_portfolio_site/mufaro.py
/Users/macbook/Desktop/WA_Cloud/mufaro.pub
/Users/macbook/Desktop/WA_Cloud/mufaro
find: /Users/macbook/Library/Application Support/firebase-heartbeat: Permission denied
find: /Users/macbook/Library/Application Support/MobileSync: Operation not permitted
find: /Users/macbook/Library/Application Support/CallHistoryTransactions: Operation not permitted
find: /Users/macbook/Library/Application Support/CloudDocs/session/db: Operation not permitted
find: /Users/macbook/Library/Application Support/com.apple.sharedfilelist: Operation not permitted
find: /Users/macbook/Library/Application Support/Knowledge: Operation not permitted
find: /Users/macbook/Library/Application Support/com.apple.TCC: Operation not permitted
find: /Users/macbook/Library/Application Support/FileProvider: Operation not permitted
find: /Users/macbook/Library/Application Support/AddressBook: Operation not permitted
find: /Users/macbook/Library/Application Support/com.apple.avfoundation/Frecents: Operation not permitted
find: /Users/macbook/Library/Application Support/CallHistoryDB: Operation not permitted
find: /Users/macbook/Library/Assistant/SiriVocabulary: Operation not permitted
find: /Users/macbook/Library/Autosave Information: Operation not permitted
find: /Users/macbook/Library/Saved Application State/com.bitnami.manager.savedState: Permission denied
find: /Users/macbook/Library/Saved Application State/com.easeus.datarecoverywizard.savedState: Permission denied
find: /Users/macbook/Library/Saved Application State/com.installbuilder.appinstaller.savedState: Permission denied
find: /Users/macbook/Library/IdentityServices: Operation not permitted
find: /Users/macbook/Library/WebKit/com.easeus.datarecoverywizard/WebsiteData/DeviceIdHashSalts/1: Permission denied
find: /Users/macbook/Library/Calendars: Operation not permitted
find: /Users/macbook/Library/Messages: Operation not permitted
find: /Users/macbook/Library/HomeKit: Operation not permitted
find: /Users/macbook/Library/Sharing: Operation not permitted
find: /Users/macbook/Library/Mail: Operation not permitted
find: /Users/macbook/Library/DuetExpertCenter: Operation not permitted
find: /Users/macbook/Library/Accounts: Operation not permitted
find: /Users/macbook/Library/Safari: Operation not permitted
find: /Users/macbook/Library/Biome: Operation not permitted
find: /Users/macbook/Library/Shortcuts: Operation not permitted
find: /Users/macbook/Library/Suggestions: Operation not permitted
find: /Users/macbook/Library/Group Containers/group.com.apple.secure-control-center-preferences: Operation not permitted
find: /Users/macbook/Library/Group Containers/group.com.apple.notes: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.VoiceMemos: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.archiveutility: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.Home: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.Safari: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.CloudDocs.MobileDocumentsFileProvider: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.mail: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.Notes: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.news: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.corerecents.recentsd/Data/Library/Recents: Operation not permitted
find: /Users/macbook/Library/Containers/com.apple.stocks: Operation not permitted
find: /Users/macbook/Library/PersonalizationPortrait: Operation not permitted
find: /Users/macbook/Library/Photos/Libraries/Syndication.photoslibrary: Operation not permitted
find: /Users/macbook/Library/Metadata/CoreSpotlight: Operation not permitted
find: /Users/macbook/Library/Metadata/com.apple.IntelligentSuggestions: Operation not permitted
find: /Users/macbook/Library/Cookies: Operation not permitted
find: /Users/macbook/Library/CoreFollowUp: Operation not permitted
find: /Users/macbook/Library/StatusKit: Operation not permitted
find: /Users/macbook/Library/Caches/com.apple.HomeKit: Operation not permitted
find: /Users/macbook/Library/Caches/CloudKit: Operation not permitted
find: /Users/macbook/Library/Caches/com.apple.Safari: Operation not permitted
find: /Users/macbook/Library/Caches/com.apple.findmy.fmfcore: Operation not permitted
find: /Users/macbook/Library/Caches/FamilyCircle: Operation not permitted
find: /Users/macbook/Library/Caches/com.apple.homed: Operation not permitted
find: /Users/macbook/Library/Caches/com.apple.findmy.fmipcore: Operation not permitted
find: /Users/macbook/Library/Caches/com.apple.ap.adprivacyd: Operation not permitted
find: /Users/macbook/.easeus/EaseUSDriver.kext: Permission denied
find: /Users/macbook/.Trash: Operation not permitted
/Users/macbook/Documents/mufarofbc.docx
/Users/macbook/Documents/mufarocbz.pdf
/Users/macbook/Downloads/mufaro.nyakudya@students.uz.ac.zw.jpeg
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~/Users/macbook/Desktop/WA_Cloud/mufaro

/Users/macbook/Users/macbook/Desktop/WA_Cloud/mufaro: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh-add ~/Desktop/WA_Cloud/mufaro  
Identity added: /Users/macbook/Desktop/WA_Cloud/mufaro (nyakudyamufa2002@gmail.com)
(base) macbook@MacBooks-MacBook-Air WA_Cloud % cat ~/mufaro.pub >> ~/.ssh/authorized_keys                          

cat: /Users/macbook/mufaro.pub: No such file or directory
(base) macbook@MacBooks-MacBook-Air WA_Cloud % cat ~/Desktop/WA_Cloud/mufaro.pub >> ~/.ssh/authorized_keys
(base) macbook@MacBooks-MacBook-Air WA_Cloud % ssh -R 80:localhost:5000 ssh.localhost.run


===============================================================================
Welcome to localhost.run!

Follow your favourite reverse tunnel at [https://twitter.com/localhost_run].

To set up and manage custom domains go to https://admin.localhost.run/

More details on custom domains (and how to enable subdomains of your custom
domain) at https://localhost.run/docs/custom-domains

If you get a permission denied error check the faq for how to connect with a key or
create a free tunnel without a key at [http://localhost:3000/docs/faq#generating-an-ssh-key].

To explore using localhost.run visit the documentation site:
https://localhost.run/docs/

===============================================================================

** your connection id is 2dfa0b16-f1d5-41da-a597-b3bb03654f7f, please mention it if you send me a message about an issue. **

authenticated as anonymous user
e3dc3d1867f352.lhr.life tunneled with tls termination, https://e3dc3d1867f352.lhr.life
create an account and add your key for a longer lasting domain name. see https://localhost.run/docs/forever-free/ for more information.
Open your tunnel address on your mobile with this QR:

## using serveo run the following command

ssh -R 80:localhost:3000 serveo.net
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                               
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      
                                                      

