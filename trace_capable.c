#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/security.h>

struct data_t {
   u32 tgid;
   u32 pid;
   u32 uid;
   int cap;
   char comm[TASK_COMM_LEN];
};

BPF_PERF_OUTPUT(events);

int kprobe__cap_capable(struct pt_regs *ctx, const struct cred *cred, struct user_namespace *targ_ns, int cap, int cap_opt) {
    u64 __pid_tgid = bpf_get_current_pid_tgid();
    u32 tgid = __pid_tgid >> 32;
    u32 pid = __pid_tgid;

    u32 uid = bpf_get_current_uid_gid();
    struct data_t data = {.tgid = tgid, .pid = pid, .uid = uid, .cap = cap};

    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    events.perf_submit(ctx, &data, sizeof(data));

    return 0;
};
