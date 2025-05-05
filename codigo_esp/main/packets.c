#include <stdio.h>
#include <string.h>


#include "esp_event.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_system.h"

#define HEADER_SIZE 12

// body size for each protocol
uint16_t data_lengths[5] = {1, 5, 15, 43, 15 + 8000*6};

char* header_packet(uint8_t transport_layer, uint8_t protocol) {
    char* header = malloc(HEADER_SIZE);
    if (header == NULL) {
        ESP_LOGE("Header", "Memory allocation failed");
        return NULL;
    }

    // 2 bytes for id
    char* id = "ID";
    memcpy(header, id, 2);

    // 6 bytes for MAC 
    uint8_t mac[6];
    esp_efuse_mac_get_default(mac);
    memcpy(header + 2, mac, 6);

    // 1 byte for transport layer
    header[8] = transport_layer;

    // 1 byte for protocol
    header[9] = protocol;

    // 2 bytes for data length
    uint16_t data_length = HEADER_SIZE + data_lengths[protocol];
    memcpy(header + 10, &data_length, 2);
    return header;
}

char* p0_packet(uint8_t layer) {
    char* packet = malloc(HEADER_SIZE + data_lengths[0]);
    char* header = header_packet(layer, 0);
    char* body = malloc(data_lengths[0]);
    // 1 byte for batt
    uint8_t batt = esp_random() % 101;
    memcpy(body, &batt, 1);

    // move header and body to packet
    memcpy(packet, header, HEADER_SIZE);
    memcpy(packet + HEADER_SIZE, body, data_lengths[0]);
    free(header);
    free(body);
    return packet;
}