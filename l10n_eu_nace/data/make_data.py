#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Numérigraphe SARL.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import csv

# List of languages to generate translations for
LANGS = ['bg','cz','da','de','ee','el','fi','fr','hr','hu','it','lt',
         'lv','mt','nl','pt','ro','ru','si','sk','sv','tr']

# All the genreated record ids will be in this forms 
ID_TEMPLATE = "nace_%s"

print "Generating the English CSV file..."
src = csv.reader(open("NACE_REV2_en.csv", "rU"))
dest = csv.writer(open("res.partner.category.csv", "w"),
                  quoting=csv.QUOTE_ALL)
# Write the file header
dest.writerow(["id", "parent_id:id", "name"])
# Write the root category
parent_ids = {0: ID_TEMPLATE % "root"}
dest.writerow([parent_ids[0], "", "NACE"])
# Skip first line
src.next()
english = {}
for row in src:
    id = ID_TEMPLATE % row[1].replace('.','_')
    name = "[%s] %s" % (row[1], row[2])
    # determine the parent
    level = int(row[0])
    parent_id = parent_ids[level-1]
    # Remember the current id as a parent
    parent_ids[level] = id
    # Remember the English name and the id
    english[id] = name
    dest.writerow([id, parent_id, name])
print "Done.\n"

for lang in LANGS:
    print "Generating the translation files for %s..."% lang
    src = csv.reader(open("NACE_REV2_%s.csv" % lang, "rU"))
    # Skip first line
    src.next()
    # Write file header
    dest = open("../i18n/%s.po" % lang, "w")
    dest.write("""# Translation of OpenERP Server.
# This file contains the translation of the following modules:
#    * l10n_eu_nace
#
msgid ""
msgstr ""
"Project-Id-Version: OpenERP Server 6.1beta\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2011-12-12 10:49+0000\\n"
"PO-Revision-Date: 2011-12-12 10:49+0000\\n"
"Last-Translator: <>\\n"
"Language-Team: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: \\n"
"Plural-Forms: \\n"

""")
    for row in src:
        name = "[%s] %s" % (row[1], row[2])
        id = ID_TEMPLATE % row[1].replace('.','_')
        dest.write(
"""#. module: l10n_eu_nace
#: model:res.partner.category,name:l10n_eu_nace.%s
msgid "%s"
msgstr "%s"

""" % (id, english[id], name) )
print "Done.\n"

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
