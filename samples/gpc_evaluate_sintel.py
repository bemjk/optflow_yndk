import numpy as np
import argparse
import glob
import os
import subprocess

FRAME_DIST = 20

assert (FRAME_DIST >= 1)


def execute(cmdlist):
    nm = []
    et = []
    ee = []
    average_num_matches = 0
    elapsed_time = 0
    average_epe = 0
    cnt = 1
    for cmd in cmdlist:
        print ('execute: ', cmd)
        res = subprocess.check_output(cmd)
        #print ('@@ result = ', res)
        outlines = res.decode().split('\n')

        nm.append( int(outlines[0].split()[1]) )
        et.append(float(outlines[1].split()[2]) )
        ee.append(float(outlines[2].split()[3]) )

        average_num_matches += nm[-1]
        elapsed_time += et[-1]
        average_epe  += ee[-1]
        for line in res.decode().split('\n'):
            print (' --> ', line)
        print ('\n!! {}: anm: {}  et: {}  aee: {}\n'.format(cnt, average_num_matches/cnt, elapsed_time, average_epe/cnt))
        cnt += 1

    average_num_matches /= len(cmdlist)
    average_epe /= len(cmdlist)
    print ('@@@ average nm: {}  total et: {}  average ee: {} from {} tests'.format(average_num_matches, elapsed_time, average_epe, len(cmdlist)))
    print ('@@@ anm = ', nm)
    print ('@@@ et  = ', et)
    print ('@@@ ee  = ', ee, ' ', np.array(ee).mean())

    return nm, et, ee




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
                        default='./valoutdir')
    parser.add_argument('--frame_dist',
                        help='Frame Skip Distance', type=int, default=20)
    args = parser.parse_args()

    try:
        os.makedirs(args.out_path)
    except OSError:
        if not os.path.isdir(args.out_path):
            raise

    print ('@ output mage will be stored in the directory {}.'.format(args.out_path))

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

            outimage = os.path.join(args.out_path, seq_name,
                                   os.path.basename(frames[i])[0:-4] + '-eval.png')

            outdir = os.path.join(args.out_path, seq_name)
            if not os.path.isdir (outdir):
                os.makedirs(outdir)
                print ('>> dir generated: ', outdir)

            cmd = [args.bin_path, '--gpu ', frames[i] , frames[i+1] , gt_flow , outimage]
            bashcmd = '  --gpu ' + frames[i] + ' ' + frames[i+1] + ' ' + gt_flow + ' ' + outimage
            cmdlist.append(cmd)
            #print (cmd)
            #print (bashcmd)
            #subprocess.check_output([args.bin_path, bashcmd])
            #input_files += [frames[i], frames[i + 1], gt_flow]
            #print ('\t\t', [frames[i], frames[i + 1], gt_flow])

    nm, et, ee = execute(cmdlist)
    with open (os.path.join(args.out_path, 'outfile.txt'), 'w') as file:
        file.write ('average_num_matches: ' + str( np.array(nm).mean()) + '\n')
        file.write ('average_endpointerr: ' + str( np.array(ee).mean()) + '\n')
        file.write ('total_elapsedtime: ' + str( np.array(et).sum()) + '\n')
        file.write ('nm= ' + str(nm) + '\n')
        file.write ('et= ' + str(et) + '\n')
        file.write ('ee= ' + str(ee) + '\n')


if __name__ == '__main__':
    print ('@@ main function issued.')
    main()
    print ('@@ finished. bye.')
