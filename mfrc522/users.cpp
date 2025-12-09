#include "users.h"



User users[] = {
  {"63768A18", "1", "manuel", "torres", "manuel.torres@gmail.com", "ALUMNO", 9 * 3600},
  {"E32F8718", "2", "antonio", "pedregal", "antonio.pedregal@gmail.com", "PROFESOR", 9 * 3600},
  {"D365E812", "3", "otoniel", "escobar", "otoniel.escobar@gmail.com", "PERSONAL_SERVICIO", 9 * 3600}
};

User* getUserFromTag(String tag) {
  for (User &u : users) {
    if (u.uid.equalsIgnoreCase(tag)) return &u;
  }
  return nullptr;
}

String evaluateAttendance(User* u) {
  return "presente";
}