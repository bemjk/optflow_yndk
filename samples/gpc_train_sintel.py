import argparse
import glob
import os
import subprocess

FRAME_DIST = 20

assert (FRAME_DIST >= 1)


def execute(cmd):
    #print ('execute: ', cmd)
    print(' -->> python subprocess starting.')
    res = subprocess.check_output(cmd)
    res = res.decode().split('\n')
    print (res)
    return

    popen = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    for stdout_line in iter(popen.stdout.readline, ''):
        print(stdout_line.rstrip())
    for stderr_line in iter(popen.stderr.readline, ''):
        print(stderr_line.rstrip())
    popen.stdout.close()
    popen.stderr.close()
    return_code = popen.wait()
    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)


def main():
    parser = argparse.ArgumentParser(
        description='Train Global Patch Collider using MPI Sintel dataset')
    parser.add_argument(
                        '--bin_path',
                        help='Path to the training executable (example_optflow_gpc_train)',
                        required=True)
    parser.add_argument('--dataset_path',
                        help='Path to the directory with frames',
                        required=True)
    parser.add_argument('--gt_path',
                        help='Path to the directory with ground truth flow',
                        required=True)
    parser.add_argument('--descriptor_type',
                        help='Descriptor type',
                        type=int,
                        default=0)
    parser.add_argument('--frame_dist',
                        help='Frame Skip Distance', type=int, default=20)
    args = parser.parse_args()

    FRAME_DIST = args.frame_dist

    print ('FRAME_DIST set to ', args.frame_dist)

    seq = glob.glob(os.path.join(args.dataset_path, '*'))
    seq.sort()
    input_files = []

    #print ('main() seq=', seq)

    for s in seq:
        seq_name = os.path.basename(s)
        frames = glob.glob(os.path.join(s, 'frame*.png'))
        frames.sort()

        #print ('s=', s)
        #print ('seq_name=', seq_name)
        #print ('frames=', frames)

        for i in range(0, len(frames) - 1, FRAME_DIST):
            gt_flow = os.path.join(args.gt_path, seq_name,
                                   os.path.basename(frames[i])[0:-4] + '.flo')
            assert (os.path.isfile(gt_flow))
            input_files += [frames[i], frames[i + 1], gt_flow]

            #print ('\t\t', [frames[i], frames[i + 1], gt_flow])

    bashcmd = 'time ' \
              + args.bin_path \
              + ' --descriptor-type=%d ' % args.descriptor_type \
              + ' --max-tree-depth=12 --print-progress=0 '

    for ifiles in input_files:
        bashcmd += '  %s' % ifiles

    print ('@@ Total {} image triplets for training (frame_dist={}).'.format(len(input_files), FRAME_DIST))
    print ('@@ run in bash: ', bashcmd)

    execute([args.bin_path, '--descriptor-type=%d' % args.descriptor_type, '--max-tree-depth=12', '--print-progress=0'] + input_files)


if __name__ == '__main__':
    print ('@@ main function issued.')
    main()
    print ('@@ finished. bye.')
