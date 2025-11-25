#include "users.h"



User users[] = {
  {"63768A18", "1", "jusepe", "hogwart", "algo1@gmail.com", 9 * 3600},
  {"E32F8718", "6", "profesor1", "MCgonagal", "algo6@gmail.com", 9 * 3600},
  {"D365E812", "11", "pservicio1", "algo1", "algo11@gmail.com", 9 * 3600}
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