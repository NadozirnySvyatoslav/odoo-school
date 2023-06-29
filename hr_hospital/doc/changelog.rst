.. _changelog:

Changelog
=========
`16.0.1.0.2`
----------------

- Fix types, added recordsets in write methods, added constraints

- Addd doctors kanban, grouped by speciality, added interns kanban

- Added visit from patient card

- Added visit from doctor kanban card

`16.0.1.0.1`
----------------

- Add abstract model person with surname, first_name, phone, email, photo, sex fields

- Update model patient with inherited person model, add birthday, age, passport, contact and personal doctor

- Update model doctor with inherited person model, add speciality

- Added model, views for diagnose

- Update disease with tree model

- Update visits model with planned_date, doctor, patient, diagnose, with blocked fields

- Add doctor_change_history model with autocreate on change doctor in patient

- Add interns to doctor models

- Add model doctor_schedule ???

- Update visit model with double dates checking

- Add wizard for bulk patient change with doctor field

- Add report with transient model

- Add the ``index.html``, ``index.rst``, ``changelog.rst`` files with the module description and changelog.

`16.0.1.0.0`
----------------

- Init version.

- Added model, views and demo data doctor

- Added model, views and demo data patient

- Added model, data for diseases

- Added model for visit