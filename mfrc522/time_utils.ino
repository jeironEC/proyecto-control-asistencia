#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 3600); // zona horaria UTC+1

void setupTime() {
  timeClient.begin();
  timeClient.setTimeOffset(3600); // España peninsular: +1h
}

String getDateTimeString() {
  timeClient.update();
  time_t epochTime = timeClient.getEpochTime();
  struct tm *ptm = gmtime((time_t *)&epochTime);

  char dateString[30];
  sprintf(dateString, "%04d-%02d-%02d %02d:%02d:%02d",
          (ptm->tm_year + 1900),
          (ptm->tm_mon + 1),
          ptm->tm_mday,
          (ptm->tm_hour + 1) % 24, // ajusta +1
          ptm->tm_min,
          ptm->tm_sec);
  return String(dateString);
}