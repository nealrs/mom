## This is a Python / Flask Quick-Start for OpenShift.

I really dig deploying Flask apps to OpenShift. But I always feel like I'm starting from scratch. So I hacked up a little quick-start repo that incorporates [derptype](https://github.com/nealrs/derptype), a minimal html doctype + styles.

## So, how do you get this running?

**Local development:**

1. Clone the repo.
2. Run `python app.py`.
3. Go to [localhost:5000](http://localhost:5000).
4. Hack your heart out!

**Deploying to OpenShift:**

1. [Sign up for OpenShift](http://openshift.com) & install the redhat command like tools: `gem install rhc`.
2. Create new OpenShift app with Python cartridge: `rhc app create myapp python-2.7`.
3. Download & unpack this repo into `myapp` directory
4. Hack, test locally, and commit _ad nauseum_
5. Push the changes to Openshift: `git push`
6. Go to http://myapp-$yournamespace.rhcloud.com

**&copy; 2014 &middot; [Neal Shyam](http://nealshyam.com) &middot; Pull requests welcome &middot; MIT License blah blah blah**
