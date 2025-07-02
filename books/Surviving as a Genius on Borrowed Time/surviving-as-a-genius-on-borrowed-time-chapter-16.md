his list to review all code base changes
from all sources. Subscribing to this list is not mandatory.
</p>
<h4 class="subheading" id="Keep-the-documentation-up-to-date_002e">Keep the documentation up to date.</h4>
<p>Update the documentation if you change behavior or add features. If you are
unsure how best to do this, send a patch to ffmpeg-devel, the documentation
maintainer(s) will review and commit your stuff.
</p>
<h4 class="subheading" id="Important-discussions-should-be-accessible-to-all_002e">Important discussions should be accessible to all.</h4>
<p>Try to keep important discussions and requests (also) on the public
developer mailing list, so that all developers can benefit from them.
</p>
<h4 class="subheading" id="Check-your-entries-in-MAINTAINERS_002e">Check your entries in MAINTAINERS.</h4>
<p>Make sure that no parts of the codebase that you maintain are missing from the
<samp class="file">MAINTAINERS</samp> file. If something that you want to maintain is missing add it with
your name after it.
If at some point you no longer want to maintain some code, then please help in
finding a new maintainer and also don&rsquo;t forget to update the <samp class="file">MAINTAINERS</samp> file.
</p>
<p>We think our rules are not too hard. If you have comments, contact us.
</p>
<a class="anchor" id="Submitting-patches"></a></div>
</div>
<div class="chapter-level-extent" id="Submitting-patches-1">
<h2 class="chapter">4 Submitting patches</h2>

<p>First, read the <a class="ref" href="#Coding-Rules">Coding Rules</a> above if you did not yet, in particular
the rules regarding patch submission.
</p>
<p>When you submit your patch, please use <code class="code">git format-patch</code> or
<code class="code">git send-email</code>. We cannot read other diffs :-).
</p>
<p>Also please do not submit a patch which contains several unrelated changes.
Split it into separate, self-contained pieces. This does not mean splitting
file by file. Instead, make the patch as small as possible while still
keeping it as a logical unit that contains an individual change, even
if it spans multiple files. This makes reviewing your patches much easier
for us and greatly increases your chances of getting your patch applied.
</p>
<p>Use the patcheck tool of FFmpeg to check your patch.
The tool is located in the tools directory.
</p>
<p>Run the <a class="ref" href="#Regression-tests">Regression tests</a> before submitting a patch in order to verify
it does not cause unexpected problems.
</p>
<p>It also helps quite a bit if you tell us what the patch does (for example
&rsquo;replaces lrint by lrintf&rsquo;), and why (for example &rsquo;*BSD isn&rsquo;t C99 compliant
and has no lrint()&rsquo;)
</p>
<p>Also please if you send several patches, send each patch as a separate mail,
do not attach several unrelated patches to the same mail.
</p>
<p>Patches should be posted to the
<a class="uref" href="https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-devel">ffmpeg-devel</a>
mailing list. Use <code class="code">git send-email</code> when possible since it will properly
send patches without requiring extra care. If you cannot, then send patches
as base64-encoded attachments, so your patch is not trashed during
transmission. Also ensure the correct mime type is used
(text/x-diff or text/x-patch or at least text/plain) and that only one
patch is inline or attached per mail.
You can check <a class="url" href="https://patchwork.ffmpeg.org">https://patchwork.ffmpeg.org</a>, if your patch does not show up, its mime type
likely was wrong.
</p>
<h4 class="subheading" id="Sending-patches-from-email-clients">Sending patches from email clients</h4>
<p>Using <code class="code">git send-email</code> might not be desirable for everyone. The
following trick allows to send patches via email clients in a safe
way. It has been tested with Outlook and Thunderbird (with X-Unsent
extension) and might work with other applications.
</p>
<p>Create your patch like this:
</p>
<pre class="verbatim">git format-patch -s -o &quot;outputfolder&quot; --add-header &quot;X-Unsent: 1&quot; --suffix .eml --to ffmpeg-devel@ffmpeg.org -1 1a2b3c4d
</pre>
<p>Now you&rsquo;ll just need to open the eml file with the email application
and execute &rsquo;Send&rsquo;.
</p>
<h4 class="subheading" id="Reviews">Reviews</h4>
<p>Your patch will be reviewed on the mailing list. You will likely be asked
to make some changes and are expected to send in an improved version that
incorporates the requests from the review. This process may go through
several iterations. Once your patch is deemed good enough, some developer
will pick it up and commit it to the official FFmpeg tree.
</p>
<p>Give us a few days to react. But if some time passes without reaction,
send a reminder by email. Your patch should eventually be dealt with.
</p>

</div>
<div class="chapter-level-extent" id="New-codecs-or-formats-checklist">
<h2 class="chapter">5 New codecs or formats checklist</h2>

<ol class="enumerate">
<li> Did you use av_cold for codec initialization and close functions?

</li><li> Did you add a long_name under NULL_IF_CONFIG_SMALL to the AVCodec or
AVInputFormat/AVOutputFormat struct?

</li><li> Did you bump the minor version number (and reset the micro version
number) in <samp class="file">libavcodec/version.h</samp> or <samp class="file">libavformat/version.h</samp>?

</li><li> Did you register it in <samp class="file">allcodecs.c</samp> or <samp class="file">allformats.c</samp>?

</li><li> Did you add the AVCodecID to <samp class="file">avcodec.h</samp>?
When adding new codec IDs, also add an entry to the codec descriptor
list in <samp class="file">libavcodec/codec_desc.c</samp>.

</li><li> If it has a FourCC, did you add it to <samp class="file">libavformat/riff.c</samp>,
even if it is only a decoder?

</li><li> Did you add a rule to compile the appropriate files in the Makefile?
Remember to do this even if you&rsquo;re just adding a format to a file that is
already being compiled by some other rule, like a raw demuxer.

</li><li> Did you add an entry to the table of supported formats or codecs in
<samp class="file">doc/general.texi</samp>?

</li><li> Did you add an entry in the Changelog?

</li><li> If it depends on a parser or a library, did you add that dependency in
configure?

</li><li> Did you <code class="code">git add</code> the appropriate files before committing?

</li><li> Did you make sure it compiles standalone, i.e. with
<code class="code">configure --disable-everything --enable-decoder=foo</code>
(or <code class="code">--enable-demuxer</code> or whatever your component is)?
</li></ol>


</div>
<div class="chapter-level-extent" id="Patch-submission-checklist">
<h2 class="chapter">6 Patch submission checklist</h2>

<ol class="enumerate">
<li> Does <code class="code">make fate</code> pass with the patch applied?

</li><li> Was the patch generated with git format-patch or send-email?

</li><li> Did you sign-off your patch? (<code class="code">git commit -s</code>)
See <a class="uref" href="https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/process/submitting-patches.rst">Sign your work</a> for the meaning
of <em class="dfn">sign-off</em>.

</li><li> Did you provide a clear git commit log message?

</li><li> Is the patch against latest FFmpeg git master branch?

</li><li> Are you subscribed to ffmpeg-devel?
(the list is subscribers only due to spam)

</li><li> Have you checked that the changes are minimal, so that the same cannot be
achieved with a smaller patch and/or simpler final code?

</li><li> If the change is to speed critical code, did you benchmark it?

</li><li> If you did any benchmarks, did you provide them in the mail?

</li><li> Have you checked that the patch does not introduce buffer overflows or
other security issues?

</li><li> Did you test your decoder or demuxer against damaged data? If no, see
tools/trasher, the noise bitstream filter, and
<a class="uref" href="http://caca.zoy.org/wiki/zzuf">zzuf</a>. Your decoder or demuxer
should not crash, end in a (near) infinite loop, or allocate ridiculous
amounts of memory when fed damaged data.

</li><li> Did you test your decoder or demuxer against sample files?
Samples may be obtained at <a class="url" href="https://samples.ffmpeg.org">https://samples.ffmpeg.org</a>.

</li><li> Does the patch not mix functional and cosmetic changes?

</li><li> Did you add tabs or trailing whitespace to the code? Both are forbidden.

</li><li> Is the patch attached to the email you send?

</li><li> Is the mime type of the patch correct? It should be text/x-diff or
text/x-patch or at least text/plain and not application/octet-stream.

</li><li> If the patch fixes a bug, did you provide a verbose analysis of the bug?

</li><li> If the patch fixes a bug, did you provide enough information, including
a sample, so the bug can be reproduced and the fix can be verified?
Note please do not attach samples &gt;100k to mails but rather provide a
URL, you can upload to <a class="url" href="https://streams.videolan.org/upload/">https://streams.videolan.org/upload/</a>.

</li><li> Did you provide a verbose summary about what the patch does change?

</li><li> Did you provide a verbose explanation why it changes things like it does?

</li><li> Did you provide a verbose summary of the user visible advantages and
disadvantages if the patch is applied?

</li><li> Did you provide an example so we can verify the new feature added by the
patch easily?

</li><li> If you added a new file, did you insert a license header? It should be
taken from FFmpeg, not randomly copied and pasted from somewhere else.

</li><li> You should maintain alphabetical order in alphabetically ordered lists as
long as doing so does not break API/ABI compatibility.

</li><li> Lines with similar content should be aligned vertically when doing so
improves readability.

</li><li> Consider adding a regression test for your code. All new modules
should be covered by tests. That includes demuxers, muxers, decoders, encoders
filters, bitstream filters, parsers. If its not possible to do that, add
an explanation why to your patchset, its ok to not test if theres a reason.

</li><li> If you added YASM code please check that things still work with &ndash;disable-yasm.

</li><li> Test your code with valgrind and or Address Sanitizer to ensure it&rsquo;s free
of leaks, out of array accesses, etc.
</li></ol>

</div>
<div class="chapter-level-extent" id="Patch-review-process">
<h2 class="chapter">7 Patch review process</h2>

<p>All patches posted to ffmpeg-devel will be reviewed, unless they contain a
clear note that the patch is not for the git master branch.
Reviews and comments will be posted as replies to the patch on the
mailing list. The patch submitter then has to take care of every comment,
that can be by resubmitting a changed patch or by discussion. Resubmitted
patches will themselves be reviewed like any other patch. If at some point
a patch passes review with no comments then it is approved, that can for
simple and small patches happen immediately while large patches will generally
have to be changed and reviewed many times before they are approved.
After a patch is approved it will be committed to the repository.
</p>
<p>We will review all submitted patches, but sometimes we are quite busy so
especially for large patches this can take several weeks.
</p>
<p>If you feel that the review process is too slow and you are willing to try to
take over maintainership of the area of code you change then just clone
git master and maintain the area of code there. We will merge each area from
where its best maintained.
</p>
<p>When resubmitting patches, please do not make any significant changes
not related to the comments received during review. Such patches will
be rejected. Instead, submit significant changes or new features as
separate patches.
</p>
<p>Everyone is welcome to review patches. Also if you are waiting for your patch
to be reviewed, please consider helping to review other patches, that is a great
way to get everyone&rsquo;s patches reviewed sooner.
</p>
<a class="anchor" id="Regression-tests"></a></div>
<div class="chapter-level-extent" id="Regression-tests-1">
<h2 class="chapter">8 Regression tests</h2>

<p>Before submitting a patch (or committing to the repository), you should at least
test that you did not break anything.
</p>
<p>Running &rsquo;make fate&rsquo; accomplishes this, please see <a class="url" href="fate.html">fate.html</a> for details.
</p>
<p>[Of course, some patches may change the results of the regression tests. In
this case, the reference results of the regression tests shall be modified
accordingly].
</p>
<ul class="mini-toc">
<li><a href="#Adding-files-to-the-fate_002dsuite-dataset" accesskey="1">Adding files to the fate-suite dataset</a></li>
<li><a href="#Visualizing-Test-Coverage" accesskey="2">Visualizing Test Coverage</a></li>
<li><a href="#Using-Valgrind" accesskey="3">Using Valgrind</a></li>
</ul>
<div class="section-level-extent" id="Adding-files-to-the-fate_002dsuite-dataset">
<h3 class="section">8.1 Adding files to the fate-suite dataset</h3>

<p>If you need a sample uploaded send a mail to samples-request.
</p>
<p>When there is no muxer or encoder available to generate test media for a
specific test then the media has to be included in the fate-suite.
First please make sure that the sample file is as small as possible to test the
respective decoder or demuxer sufficiently. Large files increase network
bandwidth and disk space requirements.
Once you have a working fate test and fate sample, provide in the commit
message or introductory message for the patch series that you post to
the ffmpeg-devel mailing list, a direct link to download the sample media.
</p>
</div>
<div class="section-level-extent" id="Visualizing-Test-Coverage">
<h3 class="section">8.2 Visualizing Test Coverage</h3>

<p>The FFmpeg build system allows visualizing the test coverage in an easy
manner with the coverage tools <code class="code">gcov</code>/<code class="code">lcov</code>.  This involves
the following steps:
</p>
<ol class="enumerate">
<li> Configure to compile with instrumentation enabled:
    <code class="code">configure --toolchain=gcov</code>.

</li><li> Run your test case, either manually or via FATE. This can be either
    the full FATE regression suite, or any arbitrary invocation of any
    front-end tool provided by FFmpeg, in any combination.

</li><li> Run <code class="code">make lcov</code> to generate coverage data in HTML format.

</li><li> View <code class="code">lcov/index.html</code> in your preferred HTML viewer.
</li></ol>

<p>You can use the command <code class="code">make lcov-reset</code> to reset the coverage
measurements. You will need to rerun <code class="code">make lcov</code> after running a
new test.
</p>
</div>
<div class="section-level-extent" id="Using-Valgrind">
<h3 class="section">8.3 Using Valgrind</h3>

<p>The configure script provides a shortcut for using valgrind to spot bugs
related to memory handling. Just add the option
<code class="code">--toolchain=valgrind-memcheck</code> or <code class="code">--toolchain=valgrind-massif</code>
to your configure line, and reasonable defaults will be set for running
FATE under the supervision of either the <strong class="strong">memcheck</strong> or the
<strong class="strong">massif</strong> tool of the valgrind suite.
</p>
<p>In case you need finer control over how valgrind is invoked, use the
<code class="code">--target-exec='valgrind &lt;your_custom_valgrind_options&gt;</code> option in
your configure line instead.
</p>
<a class="anchor" id="Release-process"></a></div>
</div>
<div class="chapter-level-extent" id="Release-process-1">
<h2 class="chapter">9 Release process</h2>

<p>FFmpeg maintains a set of <strong class="strong">release branches</strong>, which are the
recommended deliverable for system integrators and distributors (such as
Linux distributions, etc.). At regular times, a <strong class="strong">release
manager</strong> prepares, tests and publishes tarballs on the
<a class="url" href="https://ffmpeg.org">https://ffmpeg.org</a> website.
</p>
<p>There are two kinds of releases:
</p>
<ol class="enumerate">
<li> <strong class="strong">Major releases</strong> always include the latest and greatest
features and functionality.

</li><li> <strong class="strong">Point releases</strong> are cut from <strong class="strong">release</strong> branches,
which are named <code class="code">release/X</code>, with <code class="code">X</code> being the release
version number.
</li></ol>

<p>Note that we promise to our users that shared libraries from any FFmpeg
release never break programs that have been <strong class="strong">compiled</strong> against
previous versions of <strong class="strong">the same release series</strong> in any case!
</p>
<p>However, from time to time, we do make API changes that require adaptations
in applications. Such changes are only allowed in (new) major releases and
require further steps such as bumping library version numbers and/or
adjustments to the symbol versioning file. Please discuss such changes
on the <strong class="strong">ffmpeg-devel</strong> mailing list in time to allow forward planning.
</p>
<a class="anchor" id="Criteria-for-Point-Releases"></a><ul class="mini-toc">
<li><a href="#Criteria-for-Point-Releases-1" accesskey="1">Criteria for Point Releases</a></li>
<li><a href="#Release-Checklist" accesskey="2">Release Checklist</a></li>
</ul>
<div class="section-level-extent" id="Criteria-for-Point-Releases-1">
<h3 class="section">9.1 Criteria for Point Releases</h3>

<p>Changes that match the following criteria are valid candidates for
inclusion into a point release:
</p>
<ol class="enumerate">
<li> Fixes a security issue, preferably identified by a <strong class="strong">CVE
number</strong> issued by <a class="url" href="http://cve.mitre.org/">http://cve.mitre.org/</a>.

</li><li> Fixes a documented bug in <a class="url" href="https://trac.ffmpeg.org">https://trac.ffmpeg.org</a>.

</li><li> Improves the included documentation.

</li><li> Retains both source code and binary compatibility with previous
point releases of the same release branch.
</li></ol>

<p>The order for checking the rules is (1 OR 2 OR 3) AND 4.
</p>

</div>
<div class="section-level-extent" id="Release-Checklist">
<h3 class="section">9.2 Release Checklist</h3>

<p>The release process involves the following steps:
</p>
<ol class="enumerate">
<li> Ensure that the <samp class="file">RELEASE</samp> file contains the version number for
the upcoming release.

</li><li> Add the release at <a class="url" href="https://trac.ffmpeg.org/admin/ticket/versions">https://trac.ffmpeg.org/admin/ticket/versions</a>.

</li><li> Announce the intent to do a release to the mailing list.

</li><li> Make sure all relevant security fixes have been backported. See
<a class="url" href="https://ffmpeg.org/security.html">https://ffmpeg.org/security.html</a>.

</li><li> Ensure that the FATE regression suite still passes in the release
branch on at least <strong class="strong">i386</strong> and <strong class="strong">amd64</strong>
(cf. <a class="ref" href="#Regression-tests">Regression tests</a>).

</li><li> Prepare the release tarballs in <code class="code">bz2</code> and <code class="code">gz</code> formats, and
supplementing files that contain <code class="code">gpg</code> signatures

</li><li> Publish the tarballs at <a class="url" href="https://ffmpeg.org/releases">https://ffmpeg.org/releases</a>. Create and
push an annotated tag in the form <code class="code">nX</code>, with <code class="code">X</code>
containing the version number.

</li><li> Propose and send a patch to the <strong class="strong">ffmpeg-devel</strong> mailing list
with a news entry for the website.

</li><li> Publish the news entry.

</li><li> Send an announcement to the mailing list.
</li></ol>

</div>
</div>
</div>
      <p style="font-size: small;">
        This document was generated using <a class="uref" href="https://www.gnu.org/software/texinfo/"><em class="emph">makeinfo</em></a>.
      </p>
    </div>
  </body>
</html>
                                                                                                                                                                                                                                                                                            INDX( 	 ßÉa           (      Ë         €  . €m ⁄        ﬂ∆    x d     ﬁ∆    ‘∆§ÇÊ€òS|QÛ⁄“#nÇÊ€´¸mÇÊ€ ∞     ´´              b o o t s t r a p . m i n . c s s     ‡∆    p ^     ﬁ∆    aç∑ÇÊ€oÃqQÛ⁄“#nÇÊ€“#nÇÊ€ 0      €/               c o m m u n i t y . h t m l   ·∆    h X     ﬁ∆    ÆLÕÇÊ€òS|QÛ⁄“#nÇÊ€“#nÇÊ€       æ	               d e f a u l t . c s s ‚∆    p ^     ﬁ∆    2ÈÕÇÊ€oÃqQÛ⁄ÍJnÇÊ€ÍJnÇÊ€ ‡      ‰ﬁ               d e v e l o p e r . h t m l  „∆    h R     ﬁ∆    ˙ÉœÇÊ€oÃqQÛ⁄ÍJnÇÊ€ÍJnÇÊ€       ˆÎ               f a q . h t m l       ‰∆    h T     ﬁ∆    ≤[–ÇÊ€oÃqQÛ⁄ÍJnÇÊ€ÍJnÇÊ€ @      ∆=              	 f a t e . h t m l     Â∆    p `     ﬁ∆    ïΩ–ÇÊ€oÃqQÛ⁄rnÇÊ€rnÇÊ€ p(     Æl(              f f m p e g - a l l . h t m l Ê∆    ê |     ﬁ∆    ˛˜“ÇÊ€oÃqQÛ⁄rnÇÊ€rnÇÊ€ –      –¡               f f m p e g - b i t s t r e a m - f i l t e r s . h t m l     Á∆    x f     ﬁ∆    ÂY”ÇÊ€oÃqQÛ⁄rnÇÊ rnÇÊ€ ¿     <≥              f f m p e g - c o d e c s . h t m l   Ë∆    x h     ﬁ∆    ºk‘ÇÊ€oÃqQÛ⁄ônÇÊ€ônÇÊ€ ¿     ıπ              f f m p e g - d e v i c e s . h t m l È∆    x h     ﬁ∆    Gı‘ÇÊ€oÃqQÛ⁄ônÇÊ€ônÇÊ€      DÌ          