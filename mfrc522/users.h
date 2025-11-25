#ifndef USERS_H
#define USERS_H

#include <Arduino.h>

struct User {
  String uid;
  String id;
  String nombre;
  String apellido;
  String email;
  int horaEntrada;
};

User* getUserFromTag(String tag);
String evaluateAttendance(User* u);

#endif