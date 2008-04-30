#ifndef __VSERVER_H__
#define __VSERVER_H__

#define __NR_vserver 273

#include <sys/syscall.h>
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>

#define VC_CMD(c, i, v)         (((c & 0x3F) << 24) \
	                                | (((i) & 0xFF) << 16) | ((v) & 0xFFF))
#define VC_CMD_GET_VHI_NAME 	VC_CMD(2,2,0)

struct vhi_name_struct {
        uint32_t field;
        char name[65];
};

enum vhi_name_field {
        VHIN_CONTEXT=0,
        VHIN_SYSNAME,
        VHIN_NODENAME,
        VHIN_RELEASE,
        VHIN_VERSION,
        VHIN_MACHINE,
        VHIN_DOMAINNAME,
};	

uint32_t vserver(uint32_t cmd, uint32_t id, void *data)
{
	  return syscall(__NR_vserver, cmd, id, data);
}

static char stack_poison=0;

uint32_t get_vhi_name(uint32_t xid) {
	struct vhi_name_struct cmd;
	cmd.field = VHIN_CONTEXT;
	cmd.name[0]=stack_poison++;

	if (vserver(VC_CMD_GET_VHI_NAME, xid, &cmd))
		return 0;
	return (*((uint32_t *) cmd.name));
}
#endif
