/*  This file is part of the KDE project
    Copyright (C) 2009 Harald Fernengel <harry@kdevelop.org>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License version 2 as published by the Free Software Foundation.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.

*/

#ifndef SOLID_BACKENDS_IOKIT_DEVICEINTERFACE_H
#define SOLID_BACKENDS_IOKIT_DEVICEINTERFACE_H

#include <solid/ifaces/deviceinterface.h>
#include "iokitdevice.h"

#include <QtCore/QObject>
#include <QtCore/QStringList>

namespace Solid
{
namespace Backends
{
namespace IOKit
{
class DeviceInterface : public QObject, virtual public Solid::Ifaces::DeviceInterface
{
    Q_OBJECT
    Q_INTERFACES(Solid::Ifaces::DeviceInterface)
public:
    DeviceInterface(IOKitDevice *device);
    virtual ~DeviceInterface();

protected:
    IOKitDevice *m_device;
};
}
}
}

#endif // SOLID_BACKENDS_IOKIT_DEVICEINTERFACE_H
