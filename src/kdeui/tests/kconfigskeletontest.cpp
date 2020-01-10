/* This file is part of the KDE libraries
    Copyright (C) 2006 Olivier Goffart  <ogoffart at kde.org>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.
*/

#include <qtest_kde.h>
#include "kconfigskeletontest.h"
#include "kconfigskeletontest.moc"

#include <kconfig.h>
#include <kdebug.h>
#include <kstandarddirs.h>
#include <QtGui/QFont>


QTEST_KDEMAIN( KConfigSkeletonTest, GUI )

#define DEFAULT_SETTING1 false
#define DEFAULT_SETTING2 QColor(1,2,3)
#define DEFAULT_SETTING3 QFont("helvetica",12)
#define DEFAULT_SETTING4 QString("Hello World")

#define WRITE_SETTING1 true
#define WRITE_SETTING2 QColor(3,2,1)
#define WRITE_SETTING3 QFont("helvetica",14)
#define WRITE_SETTING4 QString("KDE")

void KConfigSkeletonTest::init()
{
    const QString path = KStandardDirs::locateLocal("config", "kconfigskeletontestrc");
    QFile::remove(path);
    s = new KConfigSkeleton("kconfigskeletontestrc");
    s->setCurrentGroup("MyGroup");
    itemBool = s->addItemBool("MySetting1", mMyBool, DEFAULT_SETTING1);
    s->addItemColor("MySetting2", mMyColor, DEFAULT_SETTING2);

    s->setCurrentGroup("MyOtherGroup");
    s->addItemFont("MySetting3", mMyFont, DEFAULT_SETTING3);
    s->addItemString("MySetting4", mMyString, DEFAULT_SETTING4);

    QCOMPARE(mMyBool, DEFAULT_SETTING1);
    QCOMPARE(mMyColor, DEFAULT_SETTING2);
    QCOMPARE(mMyFont, DEFAULT_SETTING3);
    QCOMPARE(mMyString, DEFAULT_SETTING4);
}

void KConfigSkeletonTest::cleanup()
{
    delete s;
}

void KConfigSkeletonTest::testSimple()
{
    mMyBool = WRITE_SETTING1;
    mMyColor = WRITE_SETTING2;
    mMyFont = WRITE_SETTING3;
    mMyString = WRITE_SETTING4;

    s->writeConfig();

    mMyBool = false;
    mMyColor = QColor();
    mMyString.clear();
    mMyFont = QFont();

    s->readConfig();

    QCOMPARE(mMyBool, WRITE_SETTING1);
    QCOMPARE(mMyColor, WRITE_SETTING2);
    QCOMPARE(mMyFont, WRITE_SETTING3);
    QCOMPARE(mMyString, WRITE_SETTING4);
}

void KConfigSkeletonTest::testDefaults()
{
    mMyBool = WRITE_SETTING1;
    mMyColor = WRITE_SETTING2;
    mMyFont = WRITE_SETTING3;
    mMyString = WRITE_SETTING4;

    s->writeConfig();

    s->setDefaults();

    QCOMPARE(mMyBool, DEFAULT_SETTING1);
    QCOMPARE(mMyColor, DEFAULT_SETTING2);
    QCOMPARE(mMyFont, DEFAULT_SETTING3);
    QCOMPARE(mMyString, DEFAULT_SETTING4);

    s->writeConfig();
}

void KConfigSkeletonTest::testKConfigDirty()
{
    itemBool->setValue(true);
    itemBool->writeConfig(s->config());
    QVERIFY(s->config()->isDirty());
    s->writeConfig();
    QVERIFY(!s->config()->isDirty());

    itemBool->setValue(false);
    itemBool->writeConfig(s->config());
    QVERIFY(s->config()->isDirty());
    s->writeConfig();
    QVERIFY(!s->config()->isDirty());
}

void KConfigSkeletonTest::testSaveRead()
{
    itemBool->setValue(true);
    s->writeConfig();

    itemBool->setValue(false);
    s->writeConfig();

    mMyBool = true;

    s->readConfig();
    QCOMPARE(mMyBool, false);
}
