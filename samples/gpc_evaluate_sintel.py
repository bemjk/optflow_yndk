import argparse
import glob
import os
import subprocess

FRAME_DIST = 20

assert (FRAME_DIST >= 1)


def execute(cmdlist):
    for cmd in cmdlist:
        print ('execute: ', cmd)
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
    parser.add_argument('--out_path',
                        help='Path to the directory of output images',
                        default='./outdir')
    parser.add_argument('--frame_dist',
                        help='Frame Skip Distance', type=int, default=20)
    args = parser.parse_args()

    FRAME_DIST = args.frame_dist

    #print ('main() args= ', args)

    seq = glob.glob(os.path.join(args.dataset_path, '*'))
    seq.sort()
    input_files = []

    cmdlist = []

    for s in seq:
        seq_name = os.path.basename(s)
        frames = glob.glob(os.path.join(s, 'frame*.png'))
        frames.sort()

        for i in range(0, len(frames) - 1, FRAME_DIST):
            gt_flow = os.path.join(args.gt_path, seq_name,
                                   os.path.basename(frames[i])[0:-4] + '.flo')
            assert (os.path.isfile(gt_flow))

            outimage = os.path.join(args.gt_path, seq_name,
                                   os.path.basename(frames[i])[0:-4] + '-eval.png')
            cmd = 'gpc_evaluate --gpu ' + frames[i] + ' ' + frames[i+1] + ' ' + gt_flow + ' ' + outimage
            cmdlist.append(cmd)
            print (cmd)
            #input_files += [frames[i], frames[i + 1], gt_flow]
            #print ('\t\t', [frames[i], frames[i + 1], gt_flow])

    #execute(cmdlist)


if __name__ == '__main__':
    print ('@@ main function issued.')
    main()
