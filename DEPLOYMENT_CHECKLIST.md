# ✅ Deployment Checklist

## Pre-Deployment

- [ ] **Environment Variables Set**
  - [ ] SECRET_KEY (strong, unique key)
  - [ ] DEBUG=False
  - [ ] ALLOWED_HOSTS (your domain)
  - [ ] Database credentials (Supabase)
  - [ ] SMSMobile API key

- [ ] **Database Ready**
  - [ ] Supabase project created
  - [ ] Database credentials obtained
  - [ ] Connection tested

- [ ] **Files Ready**
  - [ ] Procfile created
  - [ ] requirements.txt updated
  - [ ] runtime.txt created
  - [ ] settings.py configured for production

## Deployment Steps

### For Heroku:
- [ ] Install Heroku CLI
- [ ] Login to Heroku: `heroku login`
- [ ] Create app: `heroku create your-app-name`
- [ ] Set environment variables
- [ ] Deploy: `git push heroku main`
- [ ] Run migrations: `heroku run python manage.py migrate`
- [ ] Create superuser: `heroku run python manage.py createsuperuser`

### For Railway:
- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Set environment variables in dashboard
- [ ] Deploy automatically

### For Render:
- [ ] Create Render account
- [ ] Create Web Service
- [ ] Connect GitHub repository
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `gunicorn rental_management.wsgi:application`
- [ ] Set environment variables

## Post-Deployment

- [ ] **Test Application**
  - [ ] Visit deployed URL
  - [ ] Login with superuser credentials
  - [ ] Create a test tenant
  - [ ] Test SMS functionality
  - [ ] Verify all features work

- [ ] **Security Check**
  - [ ] DEBUG=False in production
  - [ ] Strong SECRET_KEY
  - [ ] HTTPS enabled
  - [ ] Environment variables secure

- [ ] **Performance Check**
  - [ ] Static files served correctly
  - [ ] Database queries optimized
  - [ ] SMS API working
  - [ ] Page load times acceptable

## Troubleshooting

### Common Issues:
- [ ] **Database Connection**: Check Supabase credentials
- [ ] **Static Files**: Run `collectstatic` command
- [ ] **SMS Not Working**: Verify API key and URL
- [ ] **Login Issues**: Check superuser creation
- [ ] **Environment Variables**: Verify all are set correctly

### Useful Commands:
```bash
# Check logs
heroku logs --tail

# Run Django shell
heroku run python manage.py shell

# Check environment variables
heroku config

# Restart app
heroku restart
```

## Success Indicators

- [ ] ✅ App loads without errors
- [ ] ✅ Login works
- [ ] ✅ Can create/edit tenants
- [ ] ✅ SMS reminders work
- [ ] ✅ Payment tracking works
- [ ] ✅ Analytics display correctly
- [ ] ✅ Archive system works

## 🎉 You're Ready!

Once all items are checked, your rental management system is successfully deployed and ready for use!


