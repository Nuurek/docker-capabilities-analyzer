#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/security.h>

const size_t maxDepth = 16;

struct data_t {
    int cap;
    int ret;
};

BPF_PERF_OUTPUT(events);

int kretprobe__cap_capable(struct pt_regs *ctx, const struct cred *cred, struct user_namespace *targ_ns, int cap, int cap_opt) {
    struct task_struct *task = (typeof(task))bpf_get_current_task();

    u32 pid;
    struct data_t data = {
        .cap = cap,
        .ret = PT_REGS_RC(ctx)
    };

    #pragma unroll
    for (int i = 0; i < 16; i++) {
        pid = task->pid;

        if (pid == CONTAINER_PID) {
            events.perf_submit(ctx, &data, sizeof(data));
            break;
        }

        if (pid == 0) {
            break;
        }

        task = task->parent;
    }

    return 0;
};
