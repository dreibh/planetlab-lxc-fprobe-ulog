#ifndef __VSERVER_H__
#define __VSERVER_H__

#include <pwd.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define VSERVER_CONFIG_PATH "/etc/vservers"
#define SLICE_ID_FILE       "slice_id"

char* get_current_username (unsigned int uid)
{
    struct passwd *passwd_entry;
    if ((passwd_entry = getpwuid(uid)) == NULL) {
        fprintf(stderr, "Could not look up user record for %d\n", uid);
        return NULL; 
    }

    return (strdup(passwd_entry->pw_name));
}

#define HASH_SIZE           (1<<12)
#define HASH_TABLE_MASK     (HASH_SIZE - 1)

struct hash_entry {
    unsigned int xid;
    uint32_t slice_id;
};

struct hash_entry slice_id_hash[HASH_SIZE];

void init_slice_id_hash() {
    memset(slice_id_hash, 0, HASH_SIZE);
}
void set_hash_entry(unsigned int xid, uint32_t slice_id) {
    int idx = xid & HASH_TABLE_MASK;
    int i;

    struct hash_entry *entry = &slice_id_hash[idx];
    if (entry->xid == 0 || entry->xid ==xid) {
        entry->slice_id = slice_id;
        entry->xid = xid;
        return;
    }

    for (i = idx+1;i!=idx;i=(i+1) & HASH_TABLE_MASK) {
        entry = &slice_id_hash[i];
        if (entry->xid == 0 || entry->xid == xid) {
            entry->slice_id = slice_id;
            entry->xid = xid;
            break;
        }
    }
}

uint32_t xid_to_slice_id_slow(unsigned int xid) {
    uint32_t slice_id;
    char *slice_name = get_current_username (xid);
    char *slice_path = (char *) malloc(sizeof(VSERVER_CONFIG_PATH) + strlen(slice_name) + sizeof(SLICE_ID_FILE) + sizeof("//"));
    sprintf(slice_path,"%s/%s/%s",VSERVER_CONFIG_PATH,slice_name,SLICE_ID_FILE);
    FILE *fp = fopen(slice_path, "r");
    if (fp) {
        fscanf(fp,"%u",&slice_id);
        set_hash_entry(xid, slice_id);
    }
    else
        slice_id = xid; // Let's leave some evidence behind, even if it's imperfect.
    fclose(fp);
    return slice_id;
}

uint32_t xid_to_slice_id_fast(unsigned int xid) {
    int idx = xid & HASH_TABLE_MASK;
    int i;
    uint32_t slice_id = 0;

    struct hash_entry *entry = &slice_id_hash[idx];
    if (entry->xid == xid)
        return entry->slice_id;

    for (i = idx+1;i!=idx;i=(i+1) & HASH_TABLE_MASK) {
        entry = &slice_id_hash[i];
        if (entry->xid == xid) {
            slice_id = entry->slice_id;
            break;
        }
    }

    return slice_id;
}

uint32_t xid_to_slice_id(unsigned int xid) {
    uint32_t slice_id;
    if (xid == 0)
        return 0;
    else if ((slice_id = xid_to_slice_id_fast(xid)) != 0)
        return slice_id;
    else
        return xid_to_slice_id_slow(xid);
}


#endif
