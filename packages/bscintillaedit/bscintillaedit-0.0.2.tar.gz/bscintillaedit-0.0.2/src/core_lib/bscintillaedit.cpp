#include "bscintillaedit.h"

#include "ScintillaEditBase.h"

#include <QDebug>
#include <QVBoxLayout>
#include <iostream>

static int PrivateCounter = 0;

class BScintillaEditPrivate : public QObject
{
    Q_DISABLE_COPY(BScintillaEditPrivate)
    Q_DECLARE_PUBLIC(BScintillaEdit)

    BScintillaEdit* const q_ptr;
    ScintillaEditBase* m_scintilla = nullptr;

public:
    explicit BScintillaEditPrivate(BScintillaEdit* const ptr) : q_ptr(ptr) {
        ++PrivateCounter;
    }

    virtual ~BScintillaEditPrivate() {
        std::cout << "~BScintillaEditPrivate(" << this << ") "
        << "(" << --PrivateCounter << " left)" << std::endl;
    }

    void setup() {
        m_scintilla = new ScintillaEditBase(q_ptr);

        auto edit = m_scintilla;
        edit->send(SCI_SETEOLMODE, SC_EOL_LF);
        edit->send(SCI_CONVERTEOLS, SC_EOL_LF);

        // Hide non-folding symbol margin (default width 16)
        edit->send(SCI_SETMARGINWIDTHN, 1, 0);

        // change linenumber color
        // color is set as 0xBBGGRR
        edit->send(SCI_STYLESETBACK, STYLE_LINENUMBER, 0xA0A0A0);

        // change the representation and color for EOL character
        // color is set as 0XAABBGGRR
        const wchar_t* nl = L"\n";
        edit->sends(SCI_SETREPRESENTATION, reinterpret_cast<uptr_t>(nl), "↩");
        edit->send(SCI_SETREPRESENTATIONCOLOUR, reinterpret_cast<uptr_t>(nl), 0xFFC0C0FF);
        edit->send(SCI_SETREPRESENTATIONAPPEARANCE, reinterpret_cast<uptr_t>(nl), SC_REPRESENTATION_COLOUR);

        connect(
            edit, &ScintillaEditBase::modified,
            this, &BScintillaEditPrivate::onModified
        );
    }

    void setLineEndVisible(bool value) {
        m_scintilla->send(SCI_SETVIEWEOL, value);
    }

    void setLineNumbersVisible(bool value) {
        // Set line number margin to display 2 digits
        // (Default width 0: invisible)
        m_scintilla->send(SCI_SETMARGINWIDTHN, 0, value ? 20 : 0);
    }

    void setLineWrapped(bool value) {
        m_scintilla->send(
            SCI_SETWRAPMODE,
            value ? SC_WRAP_WHITESPACE : SC_WRAP_NONE
        );
    }

    void setReadOnly(bool value) {
        m_scintilla->send(SCI_SETREADONLY, value);
    }

    void setRawText(const QString& value) {
        auto edit = m_scintilla;

        edit->send(SCI_SETTEXT, 0, (sptr_t)value.toUtf8().constData());
        edit->send(SCI_SETSAVEPOINT);
        edit->send(SCI_EMPTYUNDOBUFFER);
        edit->send(SCI_COLOURISE, 0, -1);
    }

    QString rawText() const
    {
        auto edit = m_scintilla;
        int textLength = edit->send(SCI_GETTEXTLENGTH);
        char * buffer = new char[textLength+1];
        edit->send(SCI_GETTEXT,textLength+1, (sptr_t)buffer);
        QString ret(buffer);
        delete [] buffer;
        return ret;
    }

    void onModified(
        Scintilla::ModificationFlags type,
        Scintilla::Position position,
        Scintilla::Position length,
        Scintilla::Position linesAdded,
        const QByteArray &text,
        Scintilla::Position line,
        Scintilla::FoldLevel foldNow,
        Scintilla::FoldLevel foldPrev
    )
    {
        Q_Q(BScintillaEdit);

        if (Scintilla::FlagSet(type, Scintilla::ModificationFlags::InsertText | Scintilla::ModificationFlags::DeleteText)) {
            auto raw_text = rawText();
            q->setTextPrivate(raw_text, false);
        }
    }
};

BScintillaEdit::BScintillaEdit(QWidget *parent)
    : QScrollArea(parent)
    , d_ptr(new BScintillaEditPrivate(this))
{
    Q_D(BScintillaEdit);

    d->setup();

    auto layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(d->m_scintilla);
    setLayout(layout);
}

BScintillaEdit::~BScintillaEdit()
{
    delete d_ptr;
}

void BScintillaEdit::setLineEndVisible(bool value)
{
    Q_D(BScintillaEdit);

    if (m_lineEndVisible == value)
        return;
    m_lineEndVisible = value;
    d->setLineEndVisible(value);
    emit lineEndVisibleChanged(m_lineEndVisible);
}

void BScintillaEdit::setLineNumbersVisible(bool value)
{
    Q_D(BScintillaEdit);

    if (m_lineNumbersVisible == value)
        return;

    m_lineNumbersVisible = value;
    d->setLineNumbersVisible(value);
    emit lineNumbersVisibleChanged(value);
}

void BScintillaEdit::setLineWrapped(bool value)
{
    Q_D(BScintillaEdit);

    if (m_lineWrapped == value)
        return;
    m_lineWrapped = value;
    d->setLineWrapped(value);
    emit lineWrappedChanged(value);
}

void BScintillaEdit::setReadOnly(bool value)
{
    Q_D(BScintillaEdit);

    if (m_readOnly == value)
        return;
    m_readOnly = value;
    d->setReadOnly(value);
    emit readOnlyChanged(value);
}

void BScintillaEdit::setText(const QString& value)
{
    setTextPrivate(value, true);
}

void BScintillaEdit::setTextPrivate(const QString &value, bool setRawText)
{
    Q_D(BScintillaEdit);

    if (m_text == value)
        return;

    m_text = value;
    if (setRawText) {
        if (m_readOnly)
            d->setReadOnly(false);
        d->setRawText(value);
        if (m_readOnly)
            d->setReadOnly(true);
    }
    emit textChanged(value);
}
