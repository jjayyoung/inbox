# Inbox

#### The next-generation email platform.


Inbox is a set of tools to make it simple to develop apps and services on top of email. This includes a modern RESTful API that return JSON and Unicode objects. See the [full API documentation](https://www.inboxapp.com/docs/api#overview) for more details.



### Set up


1. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads)

2. [Install Vagrant](http://www.vagrantup.com/downloads.html)

3. `git clone git@github.com:inboxapp/inbox.git`

4. `cd inbox`

5. `vagrant up`

    Feel free to check out the `Vagrantfile` while this starts up. It creates a host-only network for the VM at `192.168.10.200`.

6. `vagrant ssh`

    At this point you should be SSH'd into a shiny new Ubuntu 12.04 VM. The
    `inbox` directory you started with should be synced to `/vagrant`.

    If not, run `vagrant reload` and `vagrant ssh` again. You should see the
    shared folder now.

7. `cd /vagrant`

8. `bin/inbox-start`

And _voilà_! Auth an account via the commandline to start syncing:

    bin/inbox-auth ben.bitdiddle1861@gmail.com



## Provider compatibility

|  Provider  	|  Status      			| 	Details  |
|:------------	|:--------------------:	|:----------|
| Gmail 		|  :white_check_mark:	| Supported   |
| Google Apps 		|  :white_check_mark:	| Supported   |
| Microsoft Exchange | :large_blue_diamond: | Included in the [Inbox Developer Program](https://www.inboxapp.com/features)  |
| Yahoo! Mail   |  :white_check_mark:   | Supported  |
| Hotmail/Outlook.com  |  :warning:   | In development |
| AOL 	|  :warning: 			|  In development 	|
| Cyrus (Fastmail)	|  :warning:	|  In development	|
| iCloud |  :warning:	|  In development	|
| Dovecot (Gandhi) | :warning: | In development |
| Zimbra  | :no_entry:  | Not implemented |
| Courier  | :no_entry:  | Not implemented |

Please [create an issue](https://github.com/inboxapp/inbox/issues) if you use a mail provider not listed here.

## Contributing

We'd love your help making Inbox better! Join the [Google
Group](http://groups.google.com/group/inbox-dev) for project updates and feature
discussion. We also hang out in `##inbox` on `irc.freenode.net`, or you can email
[help@inboxapp.com](mailto:help@inboxapp.com).

Please sign the [Contributor License Agreement](https://www.inboxapp.com/cla.html)
before submitting patches. (It's similar to other projects, like NodeJS or Meteor.)

We maintain strict code style, following [pep8](http://legacy.python.org/dev/peps/pep-0008/), the [Google Python style
guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html), and [numpy docstring
conventions](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt).

We standardize on single-quotes for strings literals e.g. 'my-identifier', but use double-quotes for strings that are likely to contain single-quote characters as part of the string itself (such as error messages, or any strings containing natural language), e.g. "You've got an error!".


## License

This code is free software, licensed under the The GNU Affero General Public License (AGPL).
See the `LICENSE` file for more details.


#### Random notes

You should do `git config branch.master.rebase true` in the repo to keep your
history nice and clean. You can set this globally using `git config --global branch.autosetuprebase remote`.
