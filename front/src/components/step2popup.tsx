import React, { useState } from 'react';
import styled from 'styled-components';

// --- Icons ---
const InfoIcon = () => <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9.16669 6.66667H10.8334V8.33333H9.16669V6.66667ZM9.16669 10H10.8334V13.3333H9.16669V10ZM10 1.66667C5.41669 1.66667 1.66669 5.41667 1.66669 10C1.66669 14.5833 5.41669 18.3333 10 18.3333C14.5834 18.3333 18.3334 14.5833 18.3334 10C18.3334 5.41667 14.5834 1.66667 10 1.66667Z" fill="#5F00FF"/></svg>;
const EditIcon = () => <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.33331 16.6667H4.23331L12.3333 8.56667L11.4333 7.66667L3.33331 15.7667V16.6667ZM14.1333 6.76667L13.2333 5.86667L14.4 4.7C14.5833 4.51667 14.8167 4.425 15.1 4.425C15.3833 4.425 15.6167 4.51667 15.8 4.7L16.4667 5.36667C16.65 5.55 16.7416 5.78333 16.7416 6.06667C16.7416 6.35 16.65 6.58333 16.4667 6.76667L15.3 7.93333L14.1333 6.76667ZM14.1333 6.76667L4.63331 16.2667H2.49998V14.1333L12.3333 4.3L14.1333 6.76667Z" fill="#000000" /></svg>;
const LawIcon = () => <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 1.66666L2.5 5.83332V10.8333C2.5 14.5833 5.75 18.0583 10 18.3333C14.25 18.0583 17.5 14.5833 17.5 10.8333V5.83332L10 1.66666ZM10 11.6667H5V10H10V11.6667ZM10 8.33332H5V6.66666H10V8.33332Z" fill="#5F00FF"/></svg>;
const PrecedentIcon = () => <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3.33331 18.3333H16.6666V15H3.33331V18.3333ZM8.33331 1.66666L1.66665 8.33332V13.3333H5.83331V11.6667H4.16665V9.16666L8.33331 5.03332L12.5 9.16666V11.6667H10.8333V13.3333H15V8.33332L8.33331 1.66666Z" fill="#5F00FF"/></svg>;
const ChevronDownIcon = ({ expanded }: { expanded: boolean }) => (
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s ease' }}>
        <path d="M5.83331 8.33334L9.99998 12.5L14.1666 8.33334H5.83331Z" fill="#000000" />
    </svg>
);
// --- Styled Components ---
const PopupContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    margin: 0 auto;
    background: #ffffff;
    border: 1px solid #f3f4f6;
    border-radius: 40px;
    font-family: 'Pretendard', sans-serif;
    box-sizing: border-box;
    overflow: hidden;
    display: flex;
    flex-direction: column;

    *,
    *::before,
    *::after {
        box-sizing: border-box;
    }
`;

const Header = styled.div`
    padding: 18px 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    z-index: 10;
    background-color: #fff;
`;

const StatusBadge = styled.div`
    display: flex;
    align-items: center;
    gap: 4px;
    color: #ff9400;
    font-size: 14px;
    font-weight: 500;
`;

const CloseButton = styled.button`
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    font-size: 24px;
    line-height: 1;
    color: #000;
`;

const Content = styled.div`
    padding: 70px 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    overflow-y: auto;
    flex-grow: 1;
`;

const ArticleSection = styled.section`
    display: flex;
    flex-direction: column;
    gap: 4px;
`;

const ArticleTitle = styled.h2`
    font-size: 16px;
    font-weight: 600;
    color: #000000;
    margin: 0;
`;

const ArticleContent = styled.p`
    font-size: 12px;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.7);
    margin: 0;
`;

const Divider = styled.hr`
    border: none;
    height: 1px;
    background-color: #f3f4f6;
    margin: 8px 0;
`;

const SectionContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 11px;
`;

const SectionTitle = styled.h3`
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #0e0e0e;
    margin: 0;
`;

const ReasonTitleIcon = styled.span`
    color: #5f00ff;
    font-size: 20px;
    font-weight: 900;
    line-height: 1;
`;

const InfoBox = styled.div`
    padding: 24px 16px;
    background: #ffffff;
    border: 1px solid #f3f4f6;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.7);
    letter-spacing: -0.2px;
`;

const HighlightedInfoBox = styled(InfoBox)`
    background: rgba(95, 0, 255, 0.05);
    color: #5f00ff;
`;

const AccordionSection = styled.div`
    display: flex;
    flex-direction: column;
`;

const AccordionHeader = styled.button`
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    text-align: left;
    width: 100%;
`;

const AccordionContent = styled('div').withConfig({
    shouldForwardProp: (prop) => !['expanded'].includes(prop),
})<{ expanded: boolean }>`
    max-height: ${props => (props.expanded ? '1000px' : '0')};
    overflow: hidden;
    transition: max-height 0.5s ease-in-out;
    padding-top: ${props => (props.expanded ? '11px' : '0')};
`;

const ReferenceItem = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    background: #fafafa;
    border: 1px solid #f3f4f6;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.6);
`;

const ReferenceList = styled.div`
    display: flex;
    flex-direction: column;
    gap: 8px;
`;

export interface Step2PopupData {
    title: string;
    period: string;
    reason: string;
    result: string;
    strategy: string;
    laws: string[];
    precedents: string[];
}

const Step2Popup: React.FC<{
    data: Step2PopupData;
    onClose?: () => void;
    onPrev?: () => void;
    onNext?: () => void;
    showPrev?: boolean;
    showNext?: boolean;
}> = ({ data, onClose, onPrev, onNext, showPrev, showNext }) => {
    const [lawExpanded, setLawExpanded] = useState(false);
    const [precedentExpanded, setPrecedentExpanded] = useState(false);

    return (
        <PopupContainer>
            <Header>
                <StatusBadge>
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="6" cy="6" r="6" fill="#FF9400"/></svg>
                    <span>확인 필요</span>
                </StatusBadge>
                <CloseButton onClick={onClose}>×</CloseButton>
            </Header>
            <Content>
                <ArticleSection>
                    <ArticleTitle>{data.title}</ArticleTitle>
                    <ArticleContent>{data.period}</ArticleContent>
                </ArticleSection>

                <Divider />

                <SectionContainer>
                    <SectionTitle>
                        <ReasonTitleIcon>?</ReasonTitleIcon>
                        <span>이유</span>
                    </SectionTitle>
                    <InfoBox>{data.reason}</InfoBox>
                </SectionContainer>

                <SectionContainer>
                    <SectionTitle>
                        <EditIcon />
                        <span>수정 결과</span>
                    </SectionTitle>
                    <HighlightedInfoBox>
                        {data.result}
                    </HighlightedInfoBox>
                </SectionContainer>

                <SectionContainer>
                    <SectionTitle>
                        <InfoIcon />
                        <span>협상 전략 및 법적 영향</span>
                    </SectionTitle>
                    <InfoBox>
                        {data.strategy}
                    </InfoBox>
                </SectionContainer>
                
                <AccordionSection>
                    <AccordionHeader onClick={() => setLawExpanded(!lawExpanded)}>
                        <SectionTitle><LawIcon /> 참고한 법령</SectionTitle>
                        <ChevronDownIcon expanded={lawExpanded} />
                    </AccordionHeader>
                    <AccordionContent expanded={lawExpanded}>
                        <ReferenceList>
                            {data.laws.map((law, idx) => (
                                <ReferenceItem key={idx}>
                                    <span>{law}</span>
                                </ReferenceItem>
                            ))}
                        </ReferenceList>
                    </AccordionContent>
                </AccordionSection>
                
                <AccordionSection>
                    <AccordionHeader onClick={() => setPrecedentExpanded(!precedentExpanded)}>
                        <SectionTitle><PrecedentIcon /> 참고한 판례</SectionTitle>
                        <ChevronDownIcon expanded={precedentExpanded} />
                    </AccordionHeader>
                    <AccordionContent expanded={precedentExpanded}>
                        <ReferenceList>
                            {data.precedents.map((pre, idx) => (
                                <ReferenceItem key={idx}><span>{pre}</span></ReferenceItem>
                            ))}
                        </ReferenceList>
                    </AccordionContent>
                </AccordionSection>
            </Content>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '16px' }}>
                {showPrev && <button onClick={onPrev}>이전</button>}
                {showNext && <button onClick={onNext}>다음</button>}
            </div>
        </PopupContainer>
    );
};

export default Step2Popup;
